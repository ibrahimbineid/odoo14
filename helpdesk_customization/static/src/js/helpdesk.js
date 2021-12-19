odoo.define('helpdesk_customization.helpdesk', function(require) {
"use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');


    $(document).ready(function(){


        $('.ticket_region.select2').select2({
                placeholder: "Select a Region",
            });

        $('.ticket_city.select2').select2({
            placeholder: "Select a City",
          });

        $('.ticket_location.select2').select2({
            placeholder: "Select a Location",
          });

        $('.ticket_site.select2').select2({
            placeholder: "Select a Site",
          });

    //=========== Create City Option ==================================

        $('select[name=region]').on('change', function() {
            ajax.jsonRpc("/get/city_list/", 'call', {
                'region_id':$('.ticket_region option:selected').val() || false
            }).then(function (data) {
                var city = $("select[name='city']");
                if (data.city_list.length) {
                    city.html('');
                    var blankopt = $('<option>').text('')
                    city.append(blankopt);
                    _.each(data.city_list, function (x) {
                        var opt = $('<option>').text(x[1])
                        .attr('value', x[0]);
                        city.append(opt);
                    });
                    city.parent('div').show();
                }
                city.data('init', 0);
            });
        });


    //=========== Click City and Create Location Option And Select Region ==================================
        $('.ticket_city').on('change',function() {

            ajax.jsonRpc("/get/select_region/", 'call', {
                'city_id':$('.ticket_city option:selected').val() || false
            }).then(function (select_date) {
                $('select[name="region"]').val(select_date).select2();
            });

            ajax.jsonRpc("/get/location_list/", 'call', {
                'region_id':$('.ticket_region option:selected').val() || false,
                'city_id':$('.ticket_city option:selected').val() || false
            }).then(function (data) {
                var location = $("select[name='location']");
                $(".ticket_location option[value='']").attr('selected', true)
                if (data.location_list.length) {
                    location.html('');
                    var blankoptlocation = $('<option>').text('')
                    location.append(blankoptlocation);
                    _.each(data.location_list, function (x) {
                        var opt = $('<option>').text(x[1])
                        .attr('value', x[0]);
                        location.append(opt);
                    });
                    location.parent('div').show();
                }
                location.data('init', 0);
            });
        });


    //===========Click Location and Create Sites Option and Select Region and City ==================================
        $('.ticket_location').on('change',function() {
            ajax.jsonRpc("/get/select_region_city/", 'call', {
                'location_id':$('.ticket_location option:selected').val() || false,
            }).then(function (select_date) {
                $('select[name="region"]').val(select_date[0]).select2();
                ajax.jsonRpc("/get/city_list/", 'call', {
                    'region_id':$('.ticket_region option:selected').val() || false
                }).then(function (data) {
                    var city = $("select[name='city']");
                    if (data.city_list.length) {
                        city.html('');
                        var blankopt = $('<option>').text('')
                        city.append(blankopt);
                        _.each(data.city_list, function (x) {
                            var opt = $('<option>').text(x[1])
                            .attr('value', x[0]);
                            city.append(opt);
                        });
                        city.parent('div').show();
                    }
                    city.data('init', 0);
                    $('select[name="city"]').val(select_date[1]).select2();
                });
            });

            ajax.jsonRpc("/get/sites_list", 'call', {
                'region_id':$('.ticket_region option:selected').val() || false,
                'city_id':$('.ticket_city option:selected').val() || false,
                'location_id':$('.ticket_location option:selected').val() || false
            }).then(function (data) {
                var site = $("select[name='site']");
                if (data.sites_list.length) {
                    site.html('');
                    var blankoptsite = $('<option>').text('')
                    site.append(blankoptsite);
                    _.each(data.sites_list, function (x) {
                        var opt = $('<option>').text(x[1])
                        .attr('value', x[0]);
                        site.append(opt);
                    });
                    site.parent('div').show();
                }
                site.data('init', 0);
            });
        });

    // ========== click sites and Select Region , City and Location ====================
        $('.ticket_site').on('change',function() {
            ajax.jsonRpc("/get/select_region_city_location/", 'call', {
                'sites_id':$('.ticket_site option:selected').val() || false,
            }).then(function (select_date) {
                $('select[name="region"]').val(select_date[0]).select2();

                ajax.jsonRpc("/get/city_list/", 'call', {
                    'region_id':$('.ticket_region option:selected').val() || false
                }).then(function (data) {
                    var city = $("select[name='city']");
                    if (data.city_list.length) {
                        city.html('');
                        var blankopt = $('<option>').text('')
                        city.append(blankopt);
                        _.each(data.city_list, function (x) {
                            var opt = $('<option>').text(x[1])
                            .attr('value', x[0]);
                            city.append(opt);
                        });
                        city.parent('div').show();
                    }
                    city.data('init', 0);
                    $('select[name="city"]').val(select_date[1]).select2();
                });

                ajax.jsonRpc("/get/location_list/", 'call', {
                    'region_id':$('.ticket_region option:selected').val() || false,
                    'city_id':$('.ticket_city option:selected').val() || false
                }).then(function (data) {
                    var location = $("select[name='location']");
                    $(".ticket_location option[value='']").attr('selected', true)
                    if (data.location_list.length) {
                        location.html('');
                        var blankoptlocation = $('<option>').text('')
                        location.append(blankoptlocation);
                        _.each(data.location_list, function (x) {
                            var opt = $('<option>').text(x[1])
                            .attr('value', x[0]);
                            location.append(opt);
                        });
                        location.parent('div').show();
                    }
                    location.data('init', 0);
                    $('select[name="location"]').val(select_date[2]).select2();
                });
            });
        });
    });
});