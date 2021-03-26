function configureDropDownLists(ddl1, ddl2) {
  var beverages = {{ bevarr }};
  var deli = {{ deliarr }};
  var dairy = {{ dairyarr }};

  switch (ddl1.value) {
    case 'Beverages':
      ddl2.options.length = 0;
      for (i = 0; i < beverages.length; i++) {
        createOption(ddl2, beverages[i], colours[i]);
      }
      break;
    case 'Shapes':
      ddl2.options.length = 0;
      for (i = 0; i < shapes.length; i++) {
        createOption(ddl2, shapes[i], shapes[i]);
      }
      break;
    case 'Names':
      ddl2.options.length = 0;
      for (i = 0; i < names.length; i++) {
        createOption(ddl2, names[i], names[i]);
      }
      break;
    default:
      ddl2.options.length = 0;
      break;
  }

}

function createOption(ddl, text, value) {
  var opt = document.createElement('option');
  opt.value = value;
  opt.text = text;
  ddl.options.add(opt);
}

///////////

            <input type="hidden" id="hiddenid" value="" />
            <!-- <input type="hidden" name="hiddenitem" value=""> -->
            <script type="text/javascript">
            function getSelectedText(elementId) {
                var elt = document.getElementById(elementId);
                if (elt.selectedIndex == -1)
                    return null;
                return elt.options[elt.selectedIndex].text;
            }
            body.addEventListener("change click keypress", init);
            var text = "cros" //getSelectedText('itemmin');
            document.getElementById("hiddenid").value = "cros";
            </script>

///////////////////////////

        <select type="hidden" id="special">
            <option><script> special = $("#item option:selected").text(); </script></option>
        </select>