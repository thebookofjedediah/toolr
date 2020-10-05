$listButton = $('#show-list');
$mapButton = $('#show-map');
$listView = $('#list-view')
$mapView = $('#map-view')

$listButton.on('click', function() {
    $listView.show();
    $mapView.hide();
})

$mapButton.on('click', function() {
    $mapView.show();
    $listView.hide();
})