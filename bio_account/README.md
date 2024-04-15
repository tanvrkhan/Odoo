# Paper Format to configure
```
<odoo>

    <record id="paperformat_biofin" model="report.paperformat">
        <field name="name">A4 Invoice</field>
        <field name="default" eval="True"/>
        <field name="format">A4</field>
        <field name="page_height">0</field>
        <field name="page_width">0</field>
        <field name="orientation">Portrait</field>
        <field name="margin_top">3</field>
        <field name="margin_bottom">20</field>
        <field name="margin_left">7</field>
        <field name="margin_right">7</field>
        <field name="header_line" eval="False"/>
        <field name="header_spacing">0</field>
        <field name="dpi">90</field>
    </record>

</odoo>
```