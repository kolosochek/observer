var settings = new Object({
    'request_timeout': 10000, // request timeout 10s
    'refresh_timeout': 10000,//30000, // send request every 30 seconds
    'alert_file_url': "http://172.245.130.157:8000/static/observer/alert.mp3",
    'alert_file_url_ogg': '',
    'tickets_on_the_page_selector': ".b-ticket-header",
    'predefined_replies_url': "https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=managepredreplies",
    // url
    detail_mode_limit: 300
});

var observer = new Object({
    ticket_html: '',
    data: '',
    tickets_on_the_page: document.querySelectorAll(settings.tickets_on_the_page_selector),
    tickets_on_the_page_count: 0,
    tickets_expired: 0,
    timer: 0,
    set_observer: function (){
        // debug
        console.log('The observer sucsessfully set');
        // get tickets on the page
        observer.refresh_tickets_on_the_page();
        // set function that will send request and fetch results every settings.request_timeout
        observer.timer = setInterval(function(){
            observer.send_request();
        }, settings.refresh_timeout);
    },
    remove_observer: function(){
        // debug
        console.log('The observer sucsessfully removed');
        clearInterval(this.timer);
    },
    send_request: function(){
        // send request
        var request_url = window.location.href.replace("html", 'json');
        $.ajax({
            url: request_url,
            context: document.body
        }).done(function(data) {
            console.log('Send request: ' + request_url);
            // purge ticket_html from prev iteration
            observer.ticket_html = '';
            var ticket_list = data;
            // check response
            if(ticket_list instanceof Object) {
                // debug
                observer.data = ticket_list;
                observer.refresh_tickets_on_the_page();
                var tickets_in_response = ticket_list.ticket_count;
                // debug
                console.log('Tickets on the page: ' + observer.tickets_on_the_page_count);
                console.log('Tickets in response: ' + tickets_in_response);
                if (ticket_list.ticket_count > 0) {
                    for (i = 0; i < tickets_in_response; i++) {
                        var ticket = ticket_list['ticket_' + i];
                        // debug
                        //console.log("ticket #"+i);
                        //console.log(ticket);
                        var status_class = '';
                        var active = '';
                        if (ticket.ticket_status == 'Closed'){
                            status_class = 'important';
                        }
                        if (ticket.ticket_status == 'Hold'){
                            status_class = 'warning';
                        }
                        if (ticket.ticket_status == 'Open'){
                            status_class = 'success';
                        }
                        if (ticket.ticket_last_message){
                            active = 'state__active ';
                        }
                        // make raw html for each ticket
                        var ticket_html = '<tr class="'+ active +'b-ticket-header th' + ticket.ticket_id +'" id="' + ticket.ticket_id + '">' +
                            '<td class="b-ticket-id">' + ticket.ticket_id +'</td>' +
                            '<td>' +
                            '<a target="_blank" class="b-link" href="https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=viewticket&ticketid=' + ticket.ticket_id + '">' + ticket.ticket_slug + '</a>' +
                            '</td>' +
                            '<td>' +
                            '<a target="_blank" class="b-link" href="https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=viewticket&ticketid=' + ticket.ticket_id + '">' + ticket.ticket_subject + '</a>' +
                            '</td>' +
                            '<td>' + ticket.ticket_department +'</td>' +
                            '<td>' +
                            '<span class="badge bg-'+ status_class + '">' + ticket.ticket_status + '</span>' +
                                // +'important{% endif %}{% if ticket.ticket_status == 'Hold' %}warning{% endif %}{% if ticket.ticket_status == 'Open' %}success{% endif %}">{{ ticket.ticket_status }}</span>' +
                            '</td>' +
                            '</tr>';
                        //console.log(ticket_html);
                        if (ticket.ticket_last_message) {
                            // debug
                            var ticket_text = ticket.ticket_last_message.trim().replace(/\r?\n/g, "<br>").substring(0, settings.detail_mode_limit)
                            ticket_text = ticket_text.replace("<br><br>", '').replace("<br><br>", '').replace("<br><br />", '');
                            // debug
                            //console.log(ticket_text);
                            //console.log(ticket.ticket_last_message.replace(/\r?\n/g, "<br>").replace("<br><br>", "<br>"));
                            var element_state = '';
                            var message = '';
                            if (ticket.ticket_last_message) {
                                element_state = "state__active";
                                message = ticket.ticket_last_message;
                            } else {
                                element_state = "state__collapsed";
                            }
                            ticket_html += '<tr class="' + element_state + 'b-ticket-body ticket_' + ticket.ticket_id + ' tb' + ticket.ticket_id + '">' +
                            '<td class="b-ajax" colspan="5">' +
                                '<p class="b-plaintext">' + message + '</p>' +
                            '</td>' +
                            '</tr>';
                        }
                        // apply html to the ticket list html string
                        observer.ticket_html += ticket_html;
                    }
                }
                // check results
                if (observer.tickets_on_the_page_count < tickets_in_response) {
                    // debug
                    console.log('Got new ticket!');
                    // play sound
                    toolbox.play_sound();
                } else {
                    // debug
                    console.log("No new tickets");
                }
                var ticket_node = $("table tbody").eq(0);
                // clear all tickets
                ticket_node.find('tr').remove();
                // debug
                // and then append new
                ticket_node.append(observer.ticket_html);
                // refresh current tickets counter
                observer.refresh_tickets_on_the_page();
                observer.bind_events();
            }

        });

    },
    refresh_tickets_on_the_page: function(){
        observer.tickets_on_the_page_count = $(settings.tickets_on_the_page_selector).length;
        //observer.tickets_on_the_page = document.querySelectorAll(settings.tickets_on_the_page_selector);
    },
    bind_events: function(){
        var ticket_headers = $(".b-ticket-id");
        /*
        ticket_headers.on('click', function(){

            //console.log('got ticket-id click 2');
            var ticket_id = $(this).parent().attr('id');
            var ticket_header = $(".th"+ticket_id);
            var ticket_body = $(".tb"+ticket_id);
            if ($(this).parent().hasClass('state__active')){
                //console.log('collapse');
                $(this).parent().removeClass('state__active');
                ticket_body.removeClass('state__active').addClass('state__collapsed');
            } else {
                //console.log('load and expand');
                $(this).parent().addClass('state__active');
                if (!ticket_body.find('.b-plaintext').text().length){
                    $.ajax({
                        url: "http://172.245.130.157/api/byid/" + ticket_id + "/json/GDAX54ASD21afsdgDFASDHFPD117OIPUSDF",
                        context: document.body
                    }).done(function(data) {
                        if(data instanceof Object){
                            if (ticket_body.length){
                                var ticket_text = data.last_message.trim().substring(0, settings.detail_mode_limit);//.replace(/\r?\n/g, "\r\n");
                                //ticket_text = ticket_text.replace("<br><br>", '').replace("<br><br>", '').replace("<br><br />", '');
                                ticket_body.find('.b-plaintext').text(ticket_text);
                            }
                        } else {
                            console.log('got wrong response')
                        }
                    });
                } else {

                }
                ticket_body.addClass('state__active').removeClass('state__collapsed');
            }
        });
        */
    }
});
// debug
observer.bind_events();
observer.refresh_tickets_on_the_page();

// toolbox feature
function Toolbox(){}
Toolbox.prototype.play_sound = function play_sound(){
    document.getElementById("toolbox").innerHTML='<audio autoplay="autoplay"><source src="' + settings.alert_file_url + '" type="audio/mpeg" /><source src="' + settings.alert_file_url_ogg + '" type="audio/ogg" /><embed hidden="true" autostart="true" loop="false" src="' + settings.alert_file_url +'" /></audio>';
};

// create toolbox object
var toolbox = new Toolbox();


observer.bind_events();