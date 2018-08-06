$(document).ready(function() {

  $(".drop1 .option").click(function() {
    var val = $(this).attr("data-value"),
        $drop1 = $(".drop1"),
        prevActive = $(".drop1 .option.active").attr("data-value"),
        options = $(".drop1 .option").length;
    $drop1.find(".option.active").addClass("mini-hack");
    $drop1.toggleClass("visible");
    $drop1.removeClass("withBG");
    $(this).css("top");
    $drop1.toggleClass("opacity");
    $(".mini-hack").removeClass("mini-hack");
    if ($drop1.hasClass("visible")) {
      setTimeout(function() {
        $drop1.addClass("withBG");
      }, 400 + options*100);
    }
    triggerAnimation();
    if (val !== "placeholder" || prevActive === "placeholder") {
      $(".drop1 .option").removeClass("active");
      $(this).addClass("active");
    };
  });

  function triggerAnimation() {
    var finalWidth = $(".drop1").hasClass("visible") ? 19 : 18;
    $(".drop1").css("width", "18em");
    setTimeout(function() {
      $(".drop1").css("width", finalWidth + "em");
    }, 400);
  }
});
