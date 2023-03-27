$(document).ready(function () {
  // set up variables
  var startSet = false;
  var endSet = false;
  var blockedSet = false;

  // set up arrays
  var startCoords = [];
  var endCoords = [];
  var blockedCoords = [];

  // size of the grid
  var size = $("table tr").length;

  // add event listeners to table cells
  $("table td").click(function () {
    if ($("#start").is(":checked")) {
      if (startSet) {
        $("td.start").removeClass("start");
      }
      $(this).addClass("start");
      startCoords = [$(this).parent().index(), $(this).index()];
      startSet = true;
    } else if ($("#end").is(":checked")) {
      if (endSet) {
        $("td.end").removeClass("end");
      }
      $(this).addClass("end");
      endCoords = [$(this).parent().index(), $(this).index()];
      endSet = true;
    } else if ($("#blocked").is(":checked")) {
      $(this).toggleClass("blocked");
      if ($(this).hasClass("blocked")) {
        blockedCoords.push([$(this).parent().index(), $(this).index()]);
      } else {
        blockedCoords = blockedCoords.filter(
          (coord) =>
            !(
              coord[0] === $(this).parent().index() &&
              coord[1] === $(this).index()
            )
        );
      }
    }
  });

  // form submit button event listener
  $("#solve").click(function () {
    $.ajax({
      url: "/solve",
      type: "POST",
      data: JSON.stringify({
        start: startCoords,
        end: endCoords,
        blocked: blockedCoords,
        size: size,
        aplha: $("#alpha").val(),
        gamma: $("#gamma").val(),
        epsilon: $("#epsilon").val(),
        episodes: $("#episodes").val(),
      }),
      contentType: "application/json",
      success: function (response) {
        console.log(response); // log the response from the server
        $("table td").each(function () {
          var row = $(this).parent().index();
          var col = $(this).index();

          // check if the cell's coordinates match any of the coordinates in the response list
          if (response.some((coord) => coord[0] == row && coord[1] == col)) {
            $(this).addClass("path"); // add a class to the cell that changes its color
          }
        });
      },
      error: function (error) {
        console.log(error); // log any errors
      },
    });
  });

  // reset button event listener
  $("#reset").click(function () {
    $("td").removeClass();
    startSet = false;
    endSet = false;
    blockedSet = false;
    startCoords = [];
    endCoords = [];
    blockedCoords = [];
  });
});
