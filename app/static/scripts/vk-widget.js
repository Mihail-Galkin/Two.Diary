function VK_Widget_Init() {
    document.getElementById('vk_widget').innerHTML = '<div id="vk_groups"></div>';
    let style = getComputedStyle(document.documentElement, null);
    VK.Widgets.Group("vk_groups", {
        mode: 4,
        no_cover: 1,
        height: 500,
        width: "auto",
        color1: style.getPropertyValue('--block-bg'),
        color2: style.getPropertyValue('--bs-body-color'),
        color3: "5181B8"
    }, 219719675);
}

VK_Widget_Init();
window.addEventListener('load', VK_Widget_Init, false);
window.addEventListener('resize', VK_Widget_Init, false);