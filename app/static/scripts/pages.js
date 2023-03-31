function change_page(page, dest, args = {}, success = function () {
}) {
    $(dest).html('<div class="loader"></div>');
    $.ajax({
        url: "/" + page,
        type: "get",
        data: Object.assign({}, args, {"ajax": 1}),
        success: function (data) {
            $(dest).html(data);
            success();
        },
        error: function (xhr) {
            alert("error");
        }
    })
}

// Общая навигация
let pages = ["diary", "marks", "schedule", "home"];
for (let i = 0; i <= 4; i++) {
    $("body").on("click", "a." + pages[i], function () {
        if (pages[i] === "home") {
            change_page("home", "main", {}, function () {
                change_page("one-day", ".one-day-container", {"date": "today", "delta": 0});
            });
        } else {
            change_page(pages[i], "main");
        }
    })
}


// Страницы по умолчанию
change_page("home", "main", {}, function () {
    change_page("one-day", ".one-day-container", {"date": "today", "delta": 0});
});

let main = $("main"); // ближайший статичный элемент

// Окно с одним днем на главной странице
main.on("click", ".next-day", function () {
    change_page("one-day", ".one-day-container", {"date": $(".one-day").data("date"), "delta": 1})
})
main.on("click", ".prev-day", function () {
    change_page("one-day", ".one-day-container", {"date": $(".one-day").data("date"), "delta": -1})
});

// Дневник
main.on("click", ".next-week", function () {
    change_page("diary", "main", {"date": $(".date").data("date"), "delta": 7})
})
main.on("click", ".prev-week", function () {
    change_page("diary", "main", {"date": $(".date").data("date"), "delta": -7})
});


// Открытие модального окна

main.on("click", ".show-subject-modal", function (event) {
    event.stopPropagation();
    let lesson = $(this);
    change_page("subject-modal", ".modal-container", {
        "date": lesson.data("date"),
        "lesson": lesson.data("lesson")
    }, function () {
        $('#subject-modal').modal('show');
    });
});


// Оценки

main.on('change', '.marks-period-select', function (e) {
    let selected = $("option:selected", this);
    change_page("marks", "main", {
        "begin": selected.data("begin"),
        "end": selected.data("end"),
        "selected": this.value
    });
});

main.on("click", ".marks", function (event) {
    let clicked = $(this);
    let avg_mark = $(".avg-mark");
    let modal = $('#marks-modal')

    $("#marksModalLabel").html(clicked.data("subject"));
    modal.data("sum", clicked.data("sum"))
    modal.data("count", clicked.data("count"))
    modal.modal('show');

    let sum = parseInt(modal.data("sum"), 10);
    let count = parseInt(modal.data("count"), 10);

    avg_mark.html((sum / count).toFixed(2) + "");
    avg_mark.addClass("text-bg-" + Math.round(sum / count));

    if (sum / count >= 4.5 || count === 0) {
        $(".mark-raise-block").addClass("d-none");
    } else {
        let a = Math.round(sum / count) + 0.5
        $(".mark-raise").html(Math.ceil((a * count - sum) / (5 - a)) + " оценки \"5\"")
    }


});


main.on("submit", "#marks-modal", function (e) {
    e.preventDefault();
    let modal = $('#marks-modal');
    let avg_mark = $(".avg-mark");
    let sum = parseInt(modal.data("sum"), 10);
    let count = parseInt(modal.data("count"), 10);

    for (let i = 2; i <= 5; i++) {
        let n = parseInt($(".count-" + i).val(), 10);
        avg_mark.removeClass("text-bg-" + i);
        sum += n * i;
        count += n;
    }
    avg_mark.html((sum / count).toFixed(2) + "");
    avg_mark.addClass("text-bg-" + Math.round(sum / count));
});


main.on("hide.bs.modal", "#marks-modal", function () {
    let avg_mark = $(".avg-mark");
    for (let i = 2; i <= 5; i++) {
        $(".count-" + i).val("0");
        avg_mark.removeClass("text-bg-" + i);
    }
    avg_mark.html("");
    $(".mark-raise-block").removeClass("d-none");
});


// OTS

main.on("click", ".ots-next-page", function () {
    let ots = $(".ots-subjects");
    change_page("one-type-subjects", "main", {
        "subject": ots.data("subject"),
        "last-day": ots.data("last-day"),
        "first-day": ots.data("first-day"),
        "last-subject": ots.data("last-subject"),
        "first-subject": ots.data("first-subject"),
        "delta": 1,
        "page": ots.data("page")
    })
});

main.on("click", ".ots-prev-page", function () {
    let ots = $(".ots-subjects");
    change_page("one-type-subjects", "main", {
        "subject": ots.data("subject"),
        "last-day": ots.data("last-day"),
        "first-day": ots.data("first-day"),
        "last-subject": ots.data("last-subject"),
        "first-subject": ots.data("first-subject"),
        "delta": -1,
        "page": ots.data("page")
    })
});

$(".modal-container").on("click", ".open-ots", function () {
    change_page("one-type-subjects", "main", {"subject": $(this).data("subject")});
    $('#subject-modal').modal('hide');

})