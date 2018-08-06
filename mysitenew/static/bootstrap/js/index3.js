$(document).ready(function() {

  $(".drop3 .option").click(function() {
    var val = $(this).attr("data-value"),
        $drop3 = $(".drop3"),
        prevActive = $(".drop3 .option.active").attr("data-value"),
        options = $(".drop3 .option").length;
    $drop3.find(".option.active").addClass("mini-hack");
    $drop3.toggleClass("visible");
    $drop3.removeClass("withBG");
    $(this).css("top");
    $drop3.toggleClass("opacity");
    $(".mini-hack").removeClass("mini-hack");
    if ($drop3.hasClass("visible")) {
      setTimeout(function() {
        $drop3.addClass("withBG");
      }, 400 + options*100);
    }
    triggerAnimation();
    if (val !== "placeholder" || prevActive === "placeholder") {
      $(".drop3 .option").removeClass("active");
      $(this).addClass("active");
    };
  });

  function triggerAnimation() {
    var finalWidth = $(".drop3").hasClass("visible") ? 17 : 17;
    $(".drop3").css("width", "17em");
    setTimeout(function() {
      $(".drop3").css("width", finalWidth + "em");
    }, 400);
  }
});
