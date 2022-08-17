$(document).ready(function () {
  var colors = new Array(
    [255, 255, 255],
    [228, 249, 255],
    [15, 171, 188],
    [18, 202, 214],
    [250, 22, 63],
    [255, 255, 255]
  );

  var step = 0;
  //color table indices for:
  // current color left
  // next color left
  // current color right
  // next color right
  var colorIndices = [0, 1, 2, 3];

  //transition speed
  var gradientSpeed = 0.002;

  function updateGradient() {
    if ($ === undefined) return;

    var c0_0 = colors[colorIndices[0]];
    var c0_1 = colors[colorIndices[1]];
    var c1_0 = colors[colorIndices[2]];
    var c1_1 = colors[colorIndices[3]];

    var istep = 1 - step;
    var r1 = Math.round(istep * c0_0[0] + step * c0_1[0]);
    var g1 = Math.round(istep * c0_0[1] + step * c0_1[1]);
    var b1 = Math.round(istep * c0_0[2] + step * c0_1[2]);
    var color1 = "rgb(" + r1 + "," + g1 + "," + b1 + ")";

    var r2 = Math.round(istep * c1_0[0] + step * c1_1[0]);
    var g2 = Math.round(istep * c1_0[1] + step * c1_1[1]);
    var b2 = Math.round(istep * c1_0[2] + step * c1_1[2]);
    var color2 = "rgb(" + r2 + "," + g2 + "," + b2 + ")";

    $("#gradient")
      .css({
        background:
          "-webkit-gradient(linear, left top, right top, from(" +
          color1 +
          "), to(" +
          color2 +
          "))",
      })
      .css({
        background:
          "-moz-linear-gradient(left, " + color1 + " 0%, " + color2 + " 100%)",
      });

    step += gradientSpeed;
    if (step >= 1) {
      step %= 1;
      colorIndices[0] = colorIndices[1];
      colorIndices[2] = colorIndices[3];

      //pick two new target color indices
      //do not pick the same as the current one
      colorIndices[1] =
        (colorIndices[1] +
          Math.floor(1 + Math.random() * (colors.length - 1))) %
        colors.length;
      colorIndices[3] =
        (colorIndices[3] +
          Math.floor(1 + Math.random() * (colors.length - 1))) %
        colors.length;
    }
  }

  setInterval(updateGradient, 10);

  $(window).on("scroll", function () {
    var x = window.matchMedia("(min-width: 769px)");
    if (x.matches) {
      // If media query matches
      var wn = $(window).scrollTop();
      if (wn > 120) {
        $(".navbar").css("background-color", "#000000");
        $(".navbar").removeClass("py-md-3");
        $(".navbar").css("transition", "0.3s");
        $(".navbar").removeClass("mt-3");
      } else {
        $(".navbar").addClass("py-md-3");
        $(".navbar").css("background-color", "#000000");
        $(".navbar").removeClass("mt-3");
      }
    } else {
    }
  });
});

$(function () {
  var bindDatePicker = function () {
    $(".date")
      .datetimepicker({
        format: "YYYY-MM-DD",
        icons: {
          time: "fa fa-clock-o",
          date: "fa fa-calendar",
          up: "fa fa-arrow-up",
          down: "fa fa-arrow-down",
        },
      })
      .find("input:first")
      .on("blur", function () {
        // check if the date is correct. We can accept dd-mm-yyyy and yyyy-mm-dd.
        // update the format if it's yyyy-mm-dd
        var date = parseDate($(this).val());

        if (!isValidDate(date)) {
          //create date based on momentjs (we have that)
          date = moment().format("YYYY-MM-DD");
        }

        $(this).val(date);
      });
  };

  var isValidDate = function (value, format) {
    format = format || false;
    // lets parse the date to the best of our knowledge
    if (format) {
      value = parseDate(value);
    }

    var timestamp = Date.parse(value);

    return isNaN(timestamp) == false;
  };

  var parseDate = function (value) {
    var m = value.match(/^(\d{1,2})(\/|-)?(\d{1,2})(\/|-)?(\d{4})$/);
    if (m)
      value =
        m[5] + "-" + ("00" + m[3]).slice(-2) + "-" + ("00" + m[1]).slice(-2);

    return value;
  };

  bindDatePicker();
});
/* circular scroll to top - start */
(function ($) {
  "use strict";
  $(document).ready(function () {
    "use strict";

    //Scroll back to top

    var progressPath = document.querySelector(".progress-wrap path");
    var pathLength = progressPath.getTotalLength();
    progressPath.style.transition = progressPath.style.WebkitTransition =
      "none";
    progressPath.style.strokeDasharray = pathLength + " " + pathLength;
    progressPath.style.strokeDashoffset = pathLength;
    progressPath.getBoundingClientRect();
    progressPath.style.transition = progressPath.style.WebkitTransition =
      "stroke-dashoffset 10ms linear";
    var updateProgress = function () {
      var scroll = $(window).scrollTop();
      var height = $(document).height() - $(window).height();
      var progress = pathLength - (scroll * pathLength) / height;
      progressPath.style.strokeDashoffset = progress;
    };
    updateProgress();
    $(window).scroll(updateProgress);
    var offset = 50;
    var duration = 550;
    jQuery(window).on("scroll", function () {
      if (jQuery(this).scrollTop() > offset) {
        jQuery(".progress-wrap").addClass("active-progress");
      } else {
        jQuery(".progress-wrap").removeClass("active-progress");
      }
    });
    jQuery(".progress-wrap").on("click", function (event) {
      event.preventDefault();
      jQuery("html, body").animate({ scrollTop: 0 }, duration);
      return false;
    });
  });
})(jQuery);

/* navbar-new - START */
const html = document.documentElement;
const toggle = document.getElementById("toggle");
const circle = document.getElementById("bg-circle");
const navlinks = document.getElementById("navlinks");
const circleWidth = circle.clientWidth;

// Math calcul to get Height, Width, Diagonal and Circle Radius

const getVpdr = () => {
  const vph = Math.pow(html.offsetHeight, 2); // Height
  const vpw = Math.pow(html.offsetWidth, 2); // Width
  const vpd = Math.sqrt(vph + vpw); // Diagonal
  return (vpd * 2) / circleWidth; // Circle radius
};

const openNavbar = () => {
  const openTimeline = new TimelineMax();
  openTimeline.to(".navbar-new", 0, { display: "flex" });
  openTimeline.to("#bg-circle", 1.5, {
    scale: getVpdr(),
    ease: Expo.easeInOut,
  });
  openTimeline.staggerFromTo(
    ".navbar-new ul li",
    0.5,
    { y: 25, opacity: 0 },
    { y: 0, opacity: 1 },
    0.1,
    1
  );
};

const closeNavbar = () => {
  const closeTimeline = new TimelineMax();
  closeTimeline.staggerFromTo(
    ".navbar-new ul li",
    0.5,
    { y: 0, opacity: 1, delay: 0.5 },
    { y: 25, opacity: 0 },
    -0.1
  );
  closeTimeline.to("#bg-circle", 1, {
    scale: 0,
    ease: Expo.easeInOut,
    delay: -0.5,
  });
  closeTimeline.to(".navbar-new", 0, { display: "none" });
};

let isOpen = false;

toggle.onclick = function () {
  if (isOpen) {
    this.classList.remove("active");
    closeNavbar();
  } else {
    this.classList.add("active");
    openNavbar();
  }
  isOpen = !isOpen;
};
circle.onclick = function () {
  if (isOpen) {
    toggle.classList.remove("active");
    closeNavbar();
  } else {
    toggle.classList.add("active");
    closeNavbar();
  }
  isOpen = !isOpen;
};
navlinks.onclick = function () {
  if (isOpen) {
    toggle.classList.remove("active");
    closeNavbar();
  } else {
    toggle.classList.add("active");
    closeNavbar();
  }
  isOpen = !isOpen;
};

// On windows resize, recalcule circle radius and update

window.onresize = () => {
  if (isOpen) {
    gsap.to("#bg-circle", 1, { scale: getVpdr(), ease: Expo.easeInOut });
  }
};
/* Navabr - END */


/* Panel Scripts - START */
$("#panelLoader").fadeOut();
// Submit post on submit
$("#get-form").on("submit", function (event) {
  event.preventDefault();
  create_post();
});
// AJAX for posting
function create_post() {
  $.ajax({
    url: "", // the endpoint
    type: "POST", // http method
    beforeSend: function () {
      $("#panelLoader").fadeIn();
      $(".carousel").flickity("destroy");
      $("#panelShowresults").fadeOut();
    },
    data: {
      search_input: $("#search_input").val(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    }, // data sent with the post request

    // handle a successful response
    success: function (json) {
      $("#panelLoader").fadeOut();
      $("#panelShowresults").fadeIn();
      var result = $("<div/>").append(json).find("#panelShowresults").html();
      $("#panelShowresults").html(result);
      $(".carousel").flickity({
        freeScroll: true,
        contain: true,
        // disable previous & next buttons and dots
        prevNextButtons: false,
        pageDots: false,
      });
    },
  });
}
/* Panel Scripts - END */
