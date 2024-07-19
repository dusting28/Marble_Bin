function updateSelectStyle(selectId) {
  var selectElement = document.getElementById(selectId);
  var selectedOption = selectElement.options[selectElement.selectedIndex];
  
  // Get the class of the selected option
  var selectedClass = selectedOption.className;
  
  // Update the data-style attribute of the select element
  selectElement.setAttribute('class', selectedClass);
  marbleSelectContainer.innerHTML = '{{ marble_macros.marble_select('marble-select-' ~ iter1, all_marbles, 1, '') }}'.replace('color_I', selectedClass);
}