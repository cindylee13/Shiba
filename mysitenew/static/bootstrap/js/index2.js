$(document).ready(function() {

  $(".drop2 .option").click(function() {
    var val = $(this).attr("data-value"),
        $drop2 = $(".drop2"),
        prevActive = $(".drop2 .option.active").attr("data-value"),
        options = $(".drop2 .option").length;
    $drop2.find(".option.active").addClass("mini-hack");
    $drop2.toggleClass("visible");
    $drop2.removeClass("withBG");
    $(this).css("top");
    $drop2.toggleClass("opacity");
    $(".mini-hack").removeClass("mini-hack");
    if ($drop2.hasClass("visible")) {
      setTimeout(function() {
        $drop2.addClass("withBG");
      }, 400 + options*100);
    }
    triggerAnimation();
    if (val !== "placeholder" || prevActive === "placeholder") {
      $(".drop2 .option").removeClass("active");
      $(this).addClass("active");
    };
  });

  function triggerAnimation() {
    var finalWidth = $(".drop2").hasClass("visible") ? 17 : 17;
    $(".drop2").css("width", "17em");
    setTimeout(function() {
      $(".drop2").css("width", finalWidth + "em");
    }, 400);
  }
});
