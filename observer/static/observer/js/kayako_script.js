// ==UserScript==
// @name        Kayako script service pack
// @namespace   https://support.mchost.ru/support/staff/*
// @description 31337 mchost ticket system help tools pack, like fast search in predefined replies, fast search into whois or dig and even more.
// @include     https://support.mchost.ru/support/*
// @version     1.2
// @grant GM_xmlhttpRequest
// ==/UserScript==

// begin
var settings = new Object({
    'request_timeout': 10000, // request timeout 10s
    'refresh_timeout': 30000,//15000, // send request every 30 seconds
    'alert_file_url': "https://raw.githubusercontent.com/kolosochek/kayako/master/alert.mp3",
    'alert_file_url_ogg': '',
    'tickets_on_the_page_selector': "#ticketlist td.contenttableborder tr",
    'predefined_replies_url': "https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=managepredreplies",
    mass_action_backup: document.getElementById('trmassaction'),
    tickets_header_backup: document.querySelectorAll('#ticketlist td.contenttableborder tr:nth-child(1)'),
    // url
    department: 'support',
    detail_mode: 'short',
    content_type: "json",
    secret_key: "GDAX54ASD21afsdgDFASDHFPD117OIPUSDF",
    detail_mode_limit: 200
});
// get client department and status from url
var client_url = window.location.href;
var base_url = "https://support.mchost.ru/support/staff/index.php?_m=tickets&_a=manage";
client_url = client_url.replace(base_url, '');
// build reques

// inject custom css
var style = document.createElement('style');
style.innerHTML = '.observer_is_set { background: green }' +
'.observer_is_not_set { background: #E3858C }' +
'.observer_timeout { background: yellow }' +
'#toolbox { padding: 5px; position: fixed; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px; margin: 0 0 0 5px; }' +
document.body.appendChild(style);

var observer = new Object({
    ticket_html: '',
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
        // hilight_area
        highlight_area.remove_class("observer_is_set");
        highlight_area.remove_class("observer_timeout");
        highlight_area.add_class("observer_is_not_set");
    },
    send_request: function(){
        // send request
        var request_url = "http://172.245.130.157/api/goto/" + client_url + '/' + settings.detail_mode + '/' + settings.content_type + '/' + settings.secret_key;
            GM_xmlhttpRequest({
                method:     "GET",
                url:        request_url,
                data:       '',
                headers:    {
                    "Content-Type": "application/json"
                },
                onload: function (response) {
                    // hilight_area
                    highlight_area.add_class("observer_is_set");
                    highlight_area.remove_class("observer_is_not_set");
                    highlight_area.remove_class("observer_timeout");
                    // debug
                    console.log('Send request: ' + request_url);
                    // purge ticket_html from prev iteration
                    observer.ticket_html = '';
                    // parse JSON from request
                    var ticket_list = JSON.parse(response.responseText);
                    // check response
                    if(ticket_list instanceof Object){
                        var trmassaction_backup = settings.mass_action_backup.outerHTML;
                        var tickets_header_backup = settings.tickets_header_backup[0].outerHTML;
                        var ticket_inject_place = document.querySelector("#ticketlist td.contenttableborder tr");
                        // refresh current tickets counter
                        observer.refresh_tickets_on_the_page();
                        var tickets_in_response = ticket_list.ticket_count;
                        // debug
                        console.log('Tickets on the page: ' + observer.tickets_on_the_page_count);
                        console.log('Tickets in response: ' + tickets_in_response);
                        if(ticket_list.ticket_count > 0){
                            for(i=0;i<tickets_in_response;i++){
                                var ticket = ticket_list['ticket_'+i];
                                // debug
                                //console.log("ticket #"+i);
                                //console.log(ticket);
                                // make raw html for each ticket
                                var ticket_html = '<tr id="trid' + ticket.ticket_id + '" ticket="injected" class="rownotes injected_ticket" onmouseover="showHighlight(this);" onmouseout="clearHighlight(this, \'rownotes\', \'\');" onclick="if (document.ticketlist.itemhighlight' + ticket.ticket_id + '.value == \'1\') { this.className = \'rowselect\';} else { this.className = \'rownotes\';}">' +
                                    '<td align="center" valign="middle">' +
                                    '<input name="itemid[]" value="' + ticket.ticket_id + '" class="swiftcheckbox" onclick="if (document.ticketlist.itemhighlight' + ticket.ticket_id + '.value == \'0\') {document.ticketlist.itemhighlight' + ticket.ticket_id + '.value = \'1\';} else {document.ticketlist.itemhighlight' + ticket.ticket_id + '.value = \'0\';  }displayObject(\'trmassaction\');" type="checkbox">'+
                                    '<input type="hidden" name="itemhighlight' + ticket.ticket_id + '" value="0">' +
                                    '</td>' +
                                    '<td colspan="" width="80" align="center" valign="" bgcolor="">' +
                                    '<a href="index.php?_m=tickets&amp;_a=viewticket&amp;ticketid=' + ticket.ticket_id + '" target="">' + ticket.ticket_slug + '</a>'+
                                    '</td>' +
                                        // remove dateicon column
                                    '<td id="dateicon' + ticket.ticket_id + '" colspan="" width="18" align="center" valign="" bgcolor="">' +
                                    '<a id="ldateicon' + ticket.ticket_id + '" href="index.php?_m=tickets&amp;_a=viewticket&amp;ticketid=' + ticket.ticket_id + '">' +
                                    '<img src="https://support.mchost.ru/support/themes/admin_default/icon_ticket.gif" border="0">' +
                                    '</a>'+
                                    '</td>' +
                                    '<td colspan="" width="" align="left" valign="" bgcolor="">' +
                                    '<div>'+
                                        //'<span style="float:right;">' +
                                        //    '<img src="https://support.mchost.ru/support/themes/admin_default/icon_lock.gif" border="0">' +
                                        //'</span>' +
                                    '<a href="index.php?_m=tickets&amp;_a=viewticket&amp;ticketid=' + ticket.ticket_id + '" target="">'+
                                    '<img src="https://support.mchost.ru/support/themes/admin_default/icon_ticketnotselfreplied.gif" border="0" align="absmiddle">&nbsp;<img src="https://support.mchost.ru/support/themes/admin_default/icon_paperclip.gif" border="0" align="absmiddle">&nbsp;' + ticket.ticket_subject + '</a>'+
                                    '</div>' +
                                    '</td>' +
                                    '<td colspan="" width="120" align="center" valign="" bgcolor="">' + ticket.ticket_department + '</td>' +
                                    '<td colspan="" width="100" align="center" valign="" bgcolor=""><font color="#5C83B4">' + ticket.ticket_status + '</font></td>' +
                                    '<td colspan="" width="100" align="center" valign="" bgcolor=""><span class="tickettextblue">' + ticket.ticket_activity + '</span></td>' +
                                    '<td colspan="" width="80" align="center" valign="" bgcolor=""><span class="tickettextorange">' + ticket.ticket_due + '</span></td>' +
                                    '<td colspan="" width="130" align="center" valign="" bgcolor="">' + ticket.ticket_assigned + '</td>' +
                                    '<td colspan="" width="180" align="center" valign="" bgcolor="">' + ticket.ticket_email + '</td>' +
                                    '<td colspan="" width="130" align="center" valign="" bgcolor="">' + ticket.ticket_replier + '</td>' +
                                    '<td colspan="" width="18" align="center" valign="" bgcolor="">' +
                                    '<img src="https://support.mchost.ru/support/themes/admin_default/icon_flagblank.gif" width="18" height="20" border="0">' +
                                    '</td>' +
                                    '<td colspan="" width="90" align="center" valign="" bgcolor="">' +
                                    '<font color="#8A8A8A">' + ticket.ticket_priority + '</font>' +
                                    '</td>' +
                                    '</tr>';
                                // apply html to the ticket list html string
                                observer.ticket_html += ticket_html;
                                if (ticket.ticket_last_message){
                                    // debug
                                    var ticket_text = ticket.ticket_last_message.trim().replace(/\r?\n/g, "<br>").substring(0, settings.detail_mode_limit)
                                    ticket_text = ticket_text.replace("<br><br>", '').replace("<br><br>", '').replace("<br><br />", '');
                                    // debug
                                    //console.log(ticket_text);
                                    //console.log(ticket.ticket_last_message.replace(/\r?\n/g, "<br>").replace("<br><br>", "<br>"));
                                    observer.ticket_html+='' +
                                    '<tr class="rownotes ticket_' + ticket.ticket_id + ' last_message">' +
                                    '<td style="padding: 5px 10px 10px; font-size: 12px; background: #EDF4FF" colspan="13">' + ticket_text + '</td>' +
                                    '</tr>';
                                }
                            }
                        }
                        //ticket_inject_place.parentNode.innerHTML += trmassaction_backup;
                        // check results
                        if (observer.tickets_on_the_page_count < tickets_in_response){
                            // debug
                            console.log('Got new ticket!');
                            // play sound
                            toolbox.play_sound();
                        } else {
                            // debug
                            console.log("No new tickets");
                        }
                        // clear ticket table element
                        //ticket_inject_place.parentNode.innerHTML = '';
                        //ticket_inject_place = document.querySelector(".contenttableborder table tbody");
                        // debug
                        //console.log(observer.ticket_html);
                        // inject table header and mass action tr
                        //console.log(settings.trmassaction_backup[0].outerHTML);
                        var html = tickets_header_backup;
                        html += observer.ticket_html;
                        html += trmassaction_backup;
                        var ticket_node = document.querySelector(".contenttableborder table tbody");
                        ticket_node.innerHTML = html;
                        // refresh current tickets counter
                        observer.refresh_tickets_on_the_page();
                    }
                },
                // request timeout
                ontimeout: function(){
                    console.log('Timeout');
                    // hilight_area
                    highlight_area.remove_class("observer_is_set");
                    highlight_area.remove_class("observer_is_not_set");
                    highlight_area.add_class("observer_timeout");
                },
                timeout: settings.request_timeout
            });
    },
    refresh_tickets_on_the_page: function(){
        // don't forget to refresh tickets_on_the_page counter
        this.tickets_on_the_page = document.querySelectorAll(settings.tickets_on_the_page_selector);
        var tickets = this.tickets_on_the_page;
        // set number of tickets on the page
        [].forEach.call(this.tickets_on_the_page, function(ticket){
            if(ticket.id.search("trid") + 1){
                //console.log(ticket);
                ticket.setAttribute('ticket', 'injected');
                observer.tickets_on_the_page_count++;
                // debug
                //console.log(observer);
                if(ticket.style.background.search('red') + 1){
                    observer.tickets_expired++;
                    toolbox.play_sound();
                    console.log('Got expired tickets!');
                    console.log(observer.tickets_expired);
                }
            }
        });
        observer.tickets_on_the_page_count = document.querySelectorAll("#ticketlist tr[ticket='injected']").length;
        // set target="_blank" to all a elements in the ticket to open new tickets in separate tab and don't break the observer
        var tickets = this.tickets_on_the_page;
        for(i=0;i<tickets.length;i++){
            if ((tickets[i].id != '') && (tickets[i].id != "trmassaction")) {
                var links = tickets[i].querySelectorAll("a");
                for (j=0;j<links.length;j++)
                { links[j].target="_blank"}
            }
        }
    }
});
observer.refresh_tickets_on_the_page();

// toolbox feature
function Toolbox(){}
Toolbox.prototype.nodeElement = document.createElement('div');
Toolbox.prototype.toggle_button = function(button_id){
    var buttons = document.querySelectorAll("#toolbox button");
    var button_to_toggle = '';
    [].forEach.call(buttons, function(button){
        if (button.id == button_id){
            button.disabled = 'true';
            button_to_toggle = button;
        } else {
            button.disabled = '';
        }
    });
    // debug
    //console.log(buttons);
    //console.log(button_to_toggle);
    if (button_to_toggle.length){
        buttons.disabled = 'true';
    //    button_to_toggle.disabled = '';
    }
    // TODO toggle
};
Toolbox.prototype.play_sound = function play_sound(){
    document.getElementById("prcachemenu_r").innerHTML='<audio autoplay="autoplay"><source src="' + settings.alert_file_url + '" type="audio/mpeg" /><source src="' + settings.alert_file_url_ogg + '" type="audio/ogg" /><embed hidden="true" autostart="true" loop="false" src="' + settings.alert_file_url +'" /></audio>';
};
Toolbox.prototype.button_set_observer = '<button id="set_observer">Set observer</button>';
Toolbox.prototype.button_remove_observer = '<button id="remove_observer">Remove observer</button>';
Toolbox.prototype.button_mode_detail = '<button id="mode_detail">Short mode</button>';
Toolbox.prototype.button_load_ticket_list = '<button id="load_ticket_list">Load tickets</button>';

// create toolbox object
var toolbox = new Toolbox();
// debug
//console.log(toolbox);
// css
toolbox.nodeElement.id = 'toolbox';
toolbox.nodeElement.style.position = 'fixed';
toolbox.nodeElement.style.textAlign = 'center';
// apply created toolbox items
toolbox.nodeElement.innerHTML+=toolbox.button_set_observer + toolbox.button_remove_observer + "<br/>" + toolbox.button_mode_detail + toolbox.button_load_ticket_list;
document.body.insertBefore(toolbox.nodeElement, document.body.firstChild);

// bind created elements
var button_set_observer = document.getElementById('set_observer');
var button_remove_observer = document.getElementById('remove_observer');
var button_mode_detail = document.getElementById('mode_detail');
var button_load_ticket_list = document.getElementById('load_ticket_list');
// bind event listener
// set
button_set_observer.addEventListener('click', function(){
    toolbox.toggle_button("set_observer");
    observer.set_observer();
    observer.refresh_tickets_on_the_page();
});
// remove
button_remove_observer.addEventListener('click', function(){
    toolbox.toggle_button("remove_observer");
    observer.remove_observer();
    observer.refresh_tickets_on_the_page();
});
// load_ticket_list
button_load_ticket_list.addEventListener('click', function(){
    observer.send_request();
});
// mode_detail
button_mode_detail.addEventListener('click', function(){
    //console.log(settings.detail_mode);
    // toggle mode
    if (settings.detail_mode == "short"){
        settings.detail_mode = 'detail';
        this.textContent = 'Detail mode';
    } else if(settings.detail_mode == "detail"){
        settings.detail_mode = 'short'; 
        this.textContent = 'Short mode';
    }
    // load tickets
    document.getElementById("button_load_ticket_list").click();
});



//scroll top
var scrolltop = document.createElement('a');
scrolltop.textContent = "^";
scrolltop.id = 'scrolltop';
scrolltop.href = "javascript:void(0)";
scrolltop.style.position = 'fixed';
scrolltop.style.bottom = "20px";
scrolltop.style.right = "20px";
scrolltop.style.background = "#F0EADE";
scrolltop.style.color= "#6393DF";
scrolltop.style.padding = "15px";
scrolltop.style.borderRadius = "6px";

document.body.insertBefore(scrolltop, document.body.firstChild);

var scrolltop = document.getElementById('scrolltop');
// bind event listener
scrolltop.addEventListener('click', function(){
    window.scrollTo(0,0);
});

// hilight area feature
var highlight_area = new Object({
    highlight_area_element: document.getElementById("toolbox"),//("set_observer"),//("gridtableoptticketlist").nextSibling,
    toggle_class: function(className){
        this.highlight_area_element.classList.toggle(className);
    },
    remove_class: function(className){
        this.highlight_area_element.classList.remove(className);
    },
    add_class: function(className){
        this.highlight_area_element.classList.add(className);
    }
});
// by default page observer is not set
highlight_area.add_class("observer_is_not_set");