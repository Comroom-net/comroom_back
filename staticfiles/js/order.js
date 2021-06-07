function menu() {
    var url = `http://${window.location.hostname}:8080/namu/api/menu`
    $.ajax({
        tytpe: "GET",
        url: url,
        data: {},
        success: function(response) {
            console.log(response)




        }
    }).done(function(response) {
        $('#coffee').empty()
        $('#latte').empty()
        $('#ade').empty()
        $('#tea1').empty()
        var ade = []
        var tea = []
        for (var i = 0; i < response.length; i++) {
            if (response[i]['sort'] == 1 | response[i]['sort'] == 2) {
                coffeeLatte(response[i])
            } else if (response[i].sort == 3) {
                ade.push(response[i])
            } else { tea.push(response[i]) }
        }
        console.log(ade)
        console.log(tea)
        adeList(ade)



    })
}

function coffeeLatte(item) {
    console.log("coffee")
    html = `
        <tr>
            <td>${item.name}</td>
            <td>
                <button type="button" class="btn btn-outline-primary btn-sm add" id='${item.id}_ice'>ICE</button>
                <button type="button" class="btn btn-outline-danger btn-sm add" id='${item.id}_hot'>HOT</button>
            </td>
        </tr>
    `
    if (item.sort == 1) { $('#coffee').append(html) } else { $('#latte').append(html) }
}

function adeList(items) {
    html = '<tr>'
    for (var i = 0; i < items.length; i++) {
        html += `<td>
        <button type="button" class="btn btn-outline-primary btn-sm ade" id='ice_tea'>${items[i].name}</button>
    </td>`
        if (i != 0 && i % 2 == 0) {
            html += '</tr><tr>'
        }
    }
    html += '</tr>'
    $('#ade').append(html)
}



function valid_order() {
    let kart = $('#kart').text()
    kart = $.trim(kart)
    let extra = $('#request').val()
    if (kart == '' & extra == '') {
        console.log('empty')
        $('#order_fail').show()
        return false
    }
    return true
}

$(document).ready(function() {
    console.log("ordr")
    menu()

    // $('.add').click(function() {
    $(document).on("click", ".add", function() {
        console.log('add btn clicked')
        $('#order_fail').hide()
        let menu = $(this).closest("td").prev().text()
        let order_option = $(this).text()
        console.log(order_option)
        if (!order_option.includes("추가")) {
            menu += " " + order_option
        }
        let delete_icon = ' <span class="cancel"><svg class="bi bi-x-square" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\
            <path fill-rule="evenodd" d="M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>\
            <path fill-rule="evenodd" d="M11.854 4.146a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708-.708l7-7a.5.5 0 0 1 .708 0z"/>\
            <path fill-rule="evenodd" d="M4.146 4.146a.5.5 0 0 0 0 .708l7 7a.5.5 0 0 0 .708-.708l-7-7a.5.5 0 0 0-.708 0z"/>\
          </svg></span>'
        menu = "<li>" + menu + delete_icon + "</li>"
        $('#kart').append(menu)
    })
    $('.ade').click(function() {
        console.log('ade btn clicked')
        $('#order_fail').hide()
        let menu = $(this).text()
        let delete_icon = ' <span class="cancel"><svg class="bi bi-x-square" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\
            <path fill-rule="evenodd" d="M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>\
            <path fill-rule="evenodd" d="M11.854 4.146a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708-.708l7-7a.5.5 0 0 1 .708 0z"/>\
            <path fill-rule="evenodd" d="M4.146 4.146a.5.5 0 0 0 0 .708l7 7a.5.5 0 0 0 .708-.708l-7-7a.5.5 0 0 0-.708 0z"/>\
          </svg></span>'
        menu = "<li>" + menu + delete_icon + "</li>"
        $('#kart').append(menu)
    })
    $(document).on('click', 'span.cancel', function() {
        console.log("cancel clicked")
        let item = $(this).parent("li")
        item.remove()
    })
    $('#request').click(function() {
        $('#order_fail').hide()
    })

    $('#order').click(function() {
        if (valid_order()) {
            console.log('send order msg')
            let kart = $('#kart').children("li")
            let order_list = []
            jQuery.each(kart, function(i, val) {
                let menu = val.innerHTML.split("<")[0]
                console.log(menu)
                order_list.push(menu)
            })
            console.log(order_list)
            let msg = order_list.join('\n')
            console.log(msg)
            let extra = $('#request').val()
            if (extra != '') {
                extra_msg = '\n추가)\n' + extra
                msg += extra_msg
            }
            // send post to telegram api
            $('#order_list').val(msg)
            $('#order_success').show()
            $('#kart').empty()
            $('#order_form').submit()

        }

    })

})