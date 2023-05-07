(() => {
    let marksTheme = localStorage.getItem('markTheme')

    const showActiveTheme = (theme, focus = false) => {
        const btnToActive = document.querySelector(`[data-mark-theme-value="${theme}"]`)

        document.querySelectorAll('[data-mark-theme-value]').forEach(element => {
            element.classList.remove('active')
            element.setAttribute('aria-pressed', 'false')
        })

        btnToActive.classList.add('active')
        btnToActive.setAttribute('aria-pressed', 'true')
    }

    if (marksTheme !== "plain" && marksTheme !== "multicolored") {
        marksTheme = "multicolored"
    }

    document.documentElement.setAttribute('data-mark-theme', marksTheme)
    showActiveTheme(marksTheme)

    window.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('[data-mark-theme-value]')
            .forEach(toggle => {
                toggle.addEventListener('click', () => {
                    const theme = toggle.getAttribute('data-mark-theme-value')
                    localStorage.setItem('markTheme', theme)
                    document.documentElement.setAttribute('data-mark-theme', theme)
                    showActiveTheme(theme, true)
                })
            })
    })
})()