var map = L.map('map', {
    center: [48.3794, 31.1656], // Центр України
      zoom: 6,
      minZoom: 6,
      maxZoom: 6,
      maxBounds: [
        [44.0, 20.0], // Південно-західна межа (розширено вліво)
        [52.5, 42.0]  // Північно-східна межа (розширено вправо)
      ],
      maxBoundsViscosity: 1.0,
      dragging: false, 
      zoomControl: false,
      scrollWheelZoom: false, 
      doubleClickZoom: false, 
      touchZoom: false 
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    fetch('https://raw.githubusercontent.com/EugeneBorshch/ukraine_geojson/master/UA_FULL_Ukraine.geojson')
      .then(response => response.json())
      .then(data => {
        L.geoJSON(data, {
          style: function(feature) {
            return {
              color: '#3388ff', 
              weight: 2,
              fillOpacity: 0.2 
            };
          },
          onEachFeature: function(feature, layer) {
            if (feature.properties && feature.properties.name) {
              layer.bindPopup(feature.properties.name);
            }

            layer.on('click', function() {
              var regionCode = feature.properties.koatuu || 'unknown';
              window.location.href = '/regions/' + encodeURIComponent(regionCode);
            });
          }
        }).addTo(map);
      })
      .catch(error => {
        console.error('Помилка завантаження GeoJSON:', error);
      });