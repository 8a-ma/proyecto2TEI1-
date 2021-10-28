var checkboxes = document.querySelectorAll('input[type=checkbox]')
let enabledSettings = []

function CheckedTareas() {
  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
      enabledSettings =
        Array.from(checkboxes)
        .filter(i => i.checked)
        .map(i => i['name'])

      console.log(enabledSettings)
      return enabledSettings;
    })
  })
}
