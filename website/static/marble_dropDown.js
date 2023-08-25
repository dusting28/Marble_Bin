$(document).ready(function () {
  $('.scrollable-list').on('change', function () {
    const selectedValue = $(this).val();
    console.log('Selected value:', selectedValue);
    
    // Use the selectedValue in your logic
    $.ajax({
      url: '/receive_selected_value', // Flask route to handle the request
      method: 'POST',
      data: { selected_value: selectedValue }, // Send the selected value as data
      success: function (response) {
        window.location.href = response.redirect_url;
      }
    });
  });
});