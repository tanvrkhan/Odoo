import datetime
import importlib
import pyodbc
import logging
import asyncio

from contextlib import contextmanager

from odoo import models, fields, _, api,tools
from odoo.exceptions import ValidationError


assert pyodbc

class DbSync(models.Model):

    _name = 'base.db.sync.mssql'

    _description = 'Sync From MSSQL'
    _rec_name="sync_name"
    _sql_constraints = [
        ('sync_name', 'unique(sync_name)', 'Syn Name must unique!')

       ]



    sync_name=fields.Char(string='Sync Name',required=True)
    # sync_name=fields.Char('Sync Name',related='cron_id.cron_name',store=True,required=True)
    source_host = fields.Char(string='Source Host' , required=True)

    source_db_name = fields.Char(string='Source Database', required=True)

    source_user_id = fields.Char(string='Source User ID', required=True)

    source_password = fields.Char(string='Source Password', required=True)
    # @api.model
    # def _default_get_cron_id(self):
    #     cm=self.env['ir.cron'].new()        
    #     cm.active=False
    #     cm.numbercall=10
    #     cm.ir_actions_server_id.model_id=self.env['ir.model'].search([('model','=','base.db.sync.mssql')])
    #     return cm    
    cron_id=fields.Many2one('ir.cron',delegate=True, ondelete='restrict',required=True)

    # automation_enable=fields.Boolean(string='Automation Enable')

    # execute_every=fields.Selection([('m','Minutes'),('h','Hours')],string="Execute Every")
    # execute_interval=fields.Integer('Interval')

    last_updated=fields.Datetime('Last Updated')

    table_ids=fields.One2many('base.db.sync.mssql.table','ds_id')
    relation_ids=fields.One2many('base.db.sync.mssql.relation','ds_id')
    state=fields.Boolean("State")

    @api.onchange("sync_name")
    def _onchange_sync_name(self):
        if self.sync_name:

           self.cron_id.ir_actions_server_id.name='sync_from_mssql_'+self.sync_name
           
           self.cron_id.ir_actions_server_id.code="model._auto_sync('"+self.sync_name+"')"
        #    raise ValidationError(
        #     _("Error:\n" "Here is what we got instead:\n%s")
        #     % self.cron_id.ir_actions_server_id.code
        #       )       
           self.cron_id.ir_actions_server_id.model_id=self.env['ir.model'].search([('model','=','base.db.sync.mssql')])
        else:
           self.cron_id.active=False   
           self.cron_id.numbercall=-1
           self.cron_id.priority=5
           self.cron_id.doall=False

    
    
    
    
    

    # Adapters

    def connection_close(self, connection):
        return connection.close()

    def connection_open(self):
        connSTR="Driver={SQL Server};SERVER=%s,1433;DATABASE=%s;UID=%s;PWD=%s" % (self.source_host, self.source_db_name, self.source_user_id, self.source_password)
        # raise ValidationError(
        #     _("Error:\n" "Here is what we got instead:\n%s")
        #     % connSTR
        # )         
        connection= pyodbc.connect(connSTR)
        return connection

    def execute_sql(self, query,connection):
        _cursor = connection.cursor() 
        _selectRows =   _cursor.execute(query)    
        
        return _selectRows.fetchall()
    
    def connection_test(self):
        """It tests the connection

        Raises:
            Validation message with the result of the connection (fail or success)
        """
        try:
            with self.connection_open():
                pass
        except Exception as e:
            raise ValidationError(
                _("Connection test failed:\n" "Here is what we got instead:\n%s")
                % tools.ustr(e)
            ) from e
        self.state=True
        message = self.env['message.wizard'].create({'message':  _("Connection test succeeded:\n" "Everything seems properly set up!")})
        return {
        'name':  _('Successfull'),
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': 'message.wizard',
        'res_id': message.id,
        'target': 'new'
        }
        # raise ValidationError(
        #    _("Connection test succeeded:\n" "Everything seems properly set up!")
        
    
    def process_sync(self):
        def gen_table_sql(table):
            
    
            
            strcmd='select '
            for field in table.field_ids:
                strcmd=strcmd+field.source_field+','
            strcmd=strcmd[:len(strcmd)-1]
            strcmd=strcmd+' from '+table.source_table
            if table.is_initialized==True and table.update_all==False:   
              if (table.modified_stamp_field ) and self.last_updated  :
                  strcmd=strcmd + " where %s >=" %table.modified_stamp_field + "'"+self.last_updated.strftime("%Y-%m-%d")+"'"
            
                #   raise ValidationError(
                #     _("Error:\n" "Here is what we got instead:\n%s")
                #     % strcmd
                #    ) 
            
            return strcmd
        
    

        def sync_to_model(table,rowset):
           
            
            tmpmodel=self.env[table.destination_model.model]
 
            for row in rowset:
                i=0
                values=dict()
                domain=[]
                for field in table.field_ids:
                  if(field.destination_field.ttype=='selection'):
                     values[field.destination_field.name]=str(row[i])
                  else:
                     values[field.destination_field.name]=row[i]   
                  if field.is_pk:   
                     domain.append(["%s" %field.destination_field.name,'=',row[i]])
                    #   domain[field.destination_field.name]=row[i]
                  i=i+1
                if (len(domain) >0) :
                    tm=tmpmodel.search(domain)
                    if tm and (table.is_initialized==True):
                    #    values['id']=tm.id
                       tm.update(values)
                    else:
                       tmpmodel.create(values)     
                else:    
                    tmpmodel.create(values) 
            #update table status is   initialized    
            if table.is_initialized != True:  
               values=dict()
               values["is_initialized"]=1
               table.update(values)      
            if table.update_all==True:
               values=dict()
               values["update_all"]=0
               table.update(values)                 

            
        def relation_build(relation):
            
            irfields=self.env['ir.model.fields'].search(['&',('ttype','=','many2one'),('relation','=',relation.father_model.model),('model_id','=',relation.son_model.model)])
            for field in irfields:
                pass
            

            tmpmodel=self.env[relation.son_model.model]
            tmpmodel2=self.env[relation.father_model.model]
            # raise ValidationError(
            #     _("Sync from MSSQL failed:\n" "Here is what we got instead:\n%s")
            #     %tmpmodel.model
            # )            
            # tms=tmpmodel.search([('id' ,'>',0)])
            tms=tmpmodel.search([('%s' %field.name,'=',None)])
            for tm in tms:
            #     raise ValidationError(
            #    _("Sync from MSSQL failed:\n" "Here is what we got instead:\n%s")
            #      %tm.model
            #      )  
                fm=tmpmodel2.search([("%s" %relation.father_field.name,'=',getattr(tm,relation.son_field.name))])
                values=dict()
                values[field.name]=fm.id
                tm.update(values)
            
            
        # try:
        
        conn=self.connection_open()
        for table in self.table_ids:
            strcmd=gen_table_sql(table)
            rowset=  self.execute_sql(strcmd,conn)
            sync_to_model(table,rowset)
        self.connection_close(conn)    
        for rel in self.relation_ids:
            relation_build(rel)
        # except Exception as e:
        #        raise ValidationError(
        #         _("Sync from MSSQL failed:\n" "Here is what we got instead:\n%s\n%s")
        #         % (tools.ustr(e) ,strcmd)
        #        ) from e
        self.last_updated=datetime.datetime.now()    
        self.flush_recordset()    
        message = self.env['message.wizard'].create({'message':  _("Sync from MSSQL(%s-%s)  succeeded:\n" "Everything seems properly process!")%(self.source_host,self.source_db_name)})
        return {
            'name':  _('Successfull'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'res_id': message.id,
            'target': 'new'
            }              

    def _auto_sync(self,syn_name):
        syncmodel=self.search([('sync_name','=',syn_name), ('active', 'in', (True, False))])
        # raise ValidationError(
        #        _("Sync from MSSQL failed:\n" "Here is what we got instead:\n%s")
        #          % syncmodel.sync_name
        #          )         
        syncmodel.process_sync()
              
              

            
   # @api.model

   # def create(self, vals):

   #     return super(DbSync, self).create(vals)

class DBSyncTable(models.Model):

    _name = 'base.db.sync.mssql.table'

    _description = 'Sync From MSSQL Table'

    source_table=fields.Char('Source Table' , required=True)
    destination_model=fields.Many2one(
        comodel_name="ir.model",
        string="Model",    required=True  , ondelete='cascade'
    )
    ds_id=fields.Many2one('base.db.sync.mssql') 
    field_ids=fields.One2many('base.db.sync.mssql.field','dt_id')
    modified_stamp_field=fields.Char("Source Modified Stamp Field")
    is_initialized=fields.Boolean('Is Initialized',default=False)
    update_all=fields.Boolean('Update All',default=False)
    
    def action_show_details(self):
        """ Returns an action that will open a form view (in a popup) allowing to work on all the
        move lines of a particular move. This form view is used when "show operations" is not
        checked on the picking type.
        """
        # self.ensure_one()


        view = self.env.ref('sync_from_mssql.dbsync_field_tree_editable_view')
        
        return {
            'name': _('Detailed Operations'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.db.sync.mssql.table',
            # 'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id


        }
    



class DBSyncField(models.Model):

    _name = 'base.db.sync.mssql.field'

    _description = 'Sync From MSSQL Field'

    source_field=fields.Char('Source Field', required=True)

    destination_field=fields.Many2one(
        comodel_name="ir.model.fields",
        string="ModelFields",    required=True  , ondelete='cascade'
        ,domain="[('model_id','=',model_id)]"
    )
    dt_id=fields.Many2one('base.db.sync.mssql.table')     

    model_name=fields.Char("Model Name",compute='_compute_model_name') 
    model_id=fields.Integer("Model ID",compute='_compute_model_id') 
    table_name=fields.Char("Table Name",compute='_compute_table_name') 
    is_pk=fields.Boolean("IsPK")


    @api.depends("dt_id.destination_model")
    def _compute_model_name(self):
        for field in self:
            field.model_name=field.dt_id.destination_model.name
            
    @api.depends("dt_id.destination_model")
    def _compute_model_id(self):
        for field in self:
            field.model_id=field.dt_id.destination_model.id            


    @api.depends("dt_id.source_table")
    def _compute_table_name(self):
        for field in self:
            field.table_name=field.dt_id.source_table            

    # @api.onchange('dt_id')
    # def onchange_dt_id(self):
    #      domain="[('model_id','=',self.dt_id.destination_model)]"
    #      return {'domain': domain}
    
        
class DBsyncRelation(models.Model):
    _name='base.db.sync.mssql.relation'
    _description='Sync From MSSQL Relation'
    father_model=fields.Many2one(
        comodel_name="ir.model",
        string="Father Model",    required=True  , ondelete='cascade'
    )
    father_field=fields.Many2one(
        comodel_name="ir.model.fields",
        string="Father Model Field",    required=True  , ondelete='cascade'
        ,domain="[('model_id','=',father_model_id)]"
    )    
    son_model=fields.Many2one(
        comodel_name="ir.model",
        string="Son Model",    required=True  , ondelete='cascade'
    )    
    son_field=fields.Many2one(
        comodel_name="ir.model.fields",
        string="Son Model Field",    required=True  , ondelete='cascade'
        ,domain="[('model_id','=',son_model_id)]"
    ) 
    father_model_id=fields.Integer("Father Model ID",compute='_compute_father_model_id')         
    son_model_id=fields.Integer("Son Model ID",compute='_compute_son_model_id')    
    ds_id=fields.Many2one('base.db.sync.mssql') 
    @api.depends("father_model")
    def _compute_father_model_id(self):
        for rel in self:
            rel.father_model_id=rel.father_model.id   
    @api.depends("son_model")
    def _compute_son_model_id(self):
        for rel in self:
            rel.son_model_id=rel.son_model.id              

    