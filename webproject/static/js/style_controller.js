/* As soon as slider value changes call applyFilters */
$(document).on('change', 'input[type=range]', function() {
    var bright = parseInt($('#b_range1').val());//-100 to 100
    var cntrst = parseInt($('#c_range1').val());//-100 to 100
    var sharpen = parseInt($('#s_range1').val());//0 to 10
    /*
    var saturation = parseInt($('#saturation').val());//-100~100
      var vibrance = parseInt($('#Vibrance').val());//-100to 100
    var exposure = parseInt($('#Exposure').val());
    var noise = parseInt($('#Noise').val());
    var sepia = parseInt($('#Sepia').val());//0~100
    var hue = parseInt($('#Hue').val());
    var blur = parseInt($('#Blur').val());
    var clip = parseInt($('#Clip').val());
      */
    Caman('#canvas', img, function() {
      this.revert(false);
      this.brightness(bright).contrast(cntrst).sharpen(sharpen).render();
    });
  });