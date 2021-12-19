# -*- coding: utf-8 -*-

from odoo.http import content_disposition, Controller, request, route
from odoo import http
import json


#class HelpDesk(http.Controller):
#
#    @route(['/'], type='http', website=True, auth="public")
#    def get_stage_values(self):
#        values = {}
#        helpdesk_stage_obj = request.env['helpdesk.stage'].sudo().search([])
#        total = 0
#        for stage in helpdesk_stage_obj:
#            helpdesk_count_obj = request.env['helpdesk.ticket'].sudo().search_count([('stage_id.id', '=', stage.id)])
#            total += helpdesk_count_obj
#            values.update({
#                stage.name: helpdesk_count_obj,
#            })
#        values.update({
#            'جميع التذاكر': total,
#        })
#        response = request.render("Helpdesk_Dashboard_Std.homepage_test1", {'values': values})
#        return response
    
    
#class RegionFilter(http.Controller):
#    
#    @route(['/region'], type='http', website=True, auth="public")
#    def get_region_values(self):
#        values = {}
#        v_name = {}
#        cmr_name = {}
#        pmr_name = {}
#        petg_name = {}
#        cm_sitename = {}
#        pm_sitename = {}
#        helpdesk_region_obj = request.env['maintenance.region'].sudo().search([])
#
#        total = 0
#        total2 = 0
#        total3 = 0
#        for region in helpdesk_region_obj:
#            pet_count_obj = request.env['petrolling.site'].sudo().search_count([('sites_region.id', '=', region.id)])
#            pm_count_obj = request.env['maintenance.request'].sudo().search_count([('region_id.id', '=', region.id)])
#            helpdesk_count_obj = request.env['helpdesk.ticket'].sudo().search_count([('region_id.id', '=', region.id)])
#            total += helpdesk_count_obj
#            total2 += pm_count_obj
#            total3 += pet_count_obj
#            v_name.update({
#                region.name: pet_count_obj,
#            })
#          
#            cmr_name.update({
#                region.name: helpdesk_count_obj,
#            })
#            
#            pmr_name.update({
#                region.name: pm_count_obj,
#            })
#            
#            values.update({
#            'PM': total2,
#            'CM': total,
#            'Petrolling': total3,
#        })
#        
#        petrolling_group_obj = request.env['site.group'].sudo().search([])
#        for group in petrolling_group_obj:
#            pet_group_obj = request.env['petrolling.site'].sudo().search_count([('site_group_id.id', '=', group.id)])
#            petg_name.update({
#                group.name: pet_group_obj,
#            })
#            
#        cm_sitename_obj = request.env['maintenance.equipment'].sudo().search([])
#        for sitename in cm_sitename_obj:
#            cm_sname_obj = request.env['helpdesk.ticket'].sudo().search_count([('maintenance_equipment_id.id', '=', sitename.id)])
#            cm_sitename.update({
#                sitename.name: cm_sname_obj,
#            })
#            
#        pm_sitename_obj = request.env['maintenance.equipment'].sudo().search([])
#        for psitename in pm_sitename_obj:
#            pm_sname_obj = request.env['maintenance.request'].sudo().search_count([('equipment_id.id', '=', psitename.id)])
#            pm_sitename.update({
#                psitename.name: pm_sname_obj,
#            })
#            
#        response = request.render("Helpdesk_Dashboard_Std.helpdesk_sites_region", {'values1': values,'v_name': v_name,'cmr_name': cmr_name,'pmr_name': pmr_name,'petg_name': petg_name,'cm_sitename': cm_sitename,'pm_sitename': pm_sitename})
#        return response


class CM(http.Controller):

    @route(['/corrective_maintenance'], type='http', website=True, auth="public")
    def get_stage_values(self):
        values = {}
        cm_helpdesk_stage_obj = request.env['helpdesk.stage'].sudo().search([])
        total = 0
        for stage in cm_helpdesk_stage_obj:
            helpdesk_count_obj = request.env['helpdesk.ticket'].sudo().search_count([('stage_id.id', '=', stage.id)])
            total += helpdesk_count_obj
            values.update({
                stage.name: helpdesk_count_obj,
            })
        values.update({
            'All Tickets': total,
        })
        response = request.render("Helpdesk_Dashboard_Std.cm_stage_details", {'values': values})
        return response
    
    
class PM(http.Controller):

    @route(['/preventive_maintenance'], type='http', website=True, auth="public")
    def get_stage_values(self):
        values = {}
        pm_helpdesk_stage_obj = request.env['helpdesk.stage'].sudo().search([])
        total = 0
        for stage in pm_helpdesk_stage_obj:
            helpdesk_count_obj = request.env['maintenance.request'].sudo().search_count([('stage_id.id', '=', stage.id)])
            total += helpdesk_count_obj
            values.update({
                stage.name: helpdesk_count_obj,
            })
        values.update({
            'All Tickets': total,
        })
        response = request.render("Helpdesk_Dashboard_Std.pm_stage_details", {'values': values})
        return response
    
    
class Petrolling(http.Controller):

    @http.route('/petrolling', website=True, auth='public')
    def petrolling_details(self, **kw):
        petrolling_details = request.env['petrolling.site'].sudo().search([])
        return request.render("Helpdesk_Dashboard_Std.petrolling_list_details", {
            'my_details': petrolling_details
        })
    
    
class Employees(http.Controller):

    @http.route('/employees', website=True, auth='public')
    def employees_details(self, **kw):
        employees_details = request.env['hr.employee'].sudo().search([])
        return request.render("Helpdesk_Dashboard_Std.employees_list_details", {
            'my_details': employees_details
        })
    
class Users(http.Controller):

    @http.route('/users', website=True, auth='public')
    def users_details(self, **kw):
        users_details = request.env['res.users'].sudo().search([])
        return request.render("Helpdesk_Dashboard_Std.users_list_details", {
            'my_details': users_details
        })
    
    
class Contacts(http.Controller):

    @http.route('/contacts', website=True, auth='public')
    def contacts_details(self, **kw):
        contacts_details = request.env['res.partner'].sudo().search([])
        return request.render("Helpdesk_Dashboard_Std.contacts_list_details", {
            'my_details': contacts_details
        })

    
    
class AllCount(http.Controller):
    
    @route(['/'], type='http', website=True, auth="public")
    def get_region_values(self):
        values = {}
        v_name = {}
        cmr_name = {}
        pmr_name = {}
        emp_name = {}
        user_name = {}
        contacts_name = {}

    

        total = 0
        total2 = 0
        total3 = 0
        total4 = 0
        total5 = 0
        total6 = 0
        pet_count_obj = request.env['petrolling.site'].sudo().search_count([])
        pm_count_obj = request.env['maintenance.request'].sudo().search_count([])
        helpdesk_count_obj = request.env['helpdesk.ticket'].sudo().search_count([])
        emp_count_obj = request.env['hr.employee'].sudo().search_count([])
        user_count_obj = request.env['res.users'].sudo().search_count([])
        contacts_count_obj = request.env['res.partner'].sudo().search_count([])
        total += helpdesk_count_obj
        total2 += pm_count_obj
        total3 += pet_count_obj
        total4 += emp_count_obj
        total5 += user_count_obj
        total6 += contacts_count_obj

        values.update({
        'CM': total,
        'PM': total2,
        'Petrolling': total3,
        'Employees': total4,
        'Users': total5,
        'Contacts': total6,
        })
            
        response = request.render("Helpdesk_Dashboard_Std.homepage_test1", {'values1': values})
        return response