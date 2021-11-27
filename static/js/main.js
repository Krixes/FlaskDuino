function setServoDegree(s_id, s_amount) {
    let serv_deg = s_amount;
    let serv_id = s_id;

    $.post( "/pins/PWM/" + serv_id + "/" + s_amount, {

    });

    change_elem = document.getElementById(serv_id + " small");
    change_elem.innerText = "Status: " + serv_deg + "\u00B0";

    //console.log(serv_id + ": " + serv_deg + "Elem ID: " + change_elem.innerText);
}

function setPinOn(p_id) {
    let pin_id = p_id;

    $.post( "/pins/on/" + pin_id , {

    });

    change_elem = document.getElementById(pin_id + " small");
    change_elem.innerText = "Status: On";

    change_bulb = document.getElementById(pin_id + " bulb");
    change_bulb.classList.remove('bi-lightbulb-off-fill');
    change_bulb.classList.add('bi-lightbulb');

    //console.log("Turning GPIO: " + pin_id + " on.");
}

function setPinOff(p_id) {
    let pin_id = p_id;

    $.post( "/pins/off/" + pin_id , {

    });

    change_elem = document.getElementById(pin_id + " small");
    change_elem.innerText = "Status: Off";

    change_bulb = document.getElementById(pin_id + " bulb");
    change_bulb.classList.remove('bi-lightbulb');
    change_bulb.classList.add('bi-lightbulb-off-fill');

    //console.log("Turning GPIO: " + pin_id + " off.");
}