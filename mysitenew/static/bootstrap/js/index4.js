$(document).ready(function() {

  $(".drop4 .option").click(function() {
    var val = $(this).attr("data-value"),
        $drop4 = $(".drop4"),
        prevActive = $(".drop4 .option.active").attr("data-value"),
        options = $(".drop4 .option").length;
    $drop4.find(".option.active").addClass("mini-hack");
    $drop4.toggleClass("visible");
    $drop4.removeClass("withBG");
    $(this).css("top");
    $drop4.toggleClass("opacity");
    $(".mini-hack").removeClass("mini-hack");
    if ($drop4.hasClass("visible")) {
      setTimeout(function() {
        $drop4.addClass("withBG");
      }, 400 + options*100);
    }
    triggerAnimation();
    if (val !== "placeholder" || prevActive === "placeholder") {
      $(".drop4 .option").removeClass("active");
      $(this).addClass("active");
    };
  });

  function triggerAnimation() {
    var finalWidth = $(".drop4").hasClass("visible") ? 17 : 17;
    $(".drop4").css("width", "17em");
    setTimeout(function() {
      $(".drop4").css("width", finalWidth + "em");
    }, 400);
  }
});
