$("#togglePassword").click(function (e) {
    let password = $(".password-field");
    if (password.attr("type") === "password") { password.get(0).type = "text"; }
    else { password.get(0).type = "password"; }
})