$(document).ready(function () {
  $('.selectpicker').selectpicker();

  $('#marbles_select').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    var selectedValue = $(this).find('option').eq(clickedIndex).val();
    
    // Use the selectedValue in your logic
    $.ajax({
      url: '/receive_selected_value', // Flask route to handle the request
      method: 'POST',
      data: { selected_value: selectedValue }, // Send the selected value as data
      success: function (response) {
        window.location.href = response.redirect_url;
      }
    });

  });;
});