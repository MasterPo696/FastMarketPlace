let map, marker;

document.addEventListener('DOMContentLoaded', function() {
    // Load required scripts dynamically
    loadScript('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js')
        .then(() => loadScript('https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js'))
        .then(() => {
            // Initialize map when modal opens
            const addressModal = document.getElementById('addressModal');
            if (addressModal) {
                addressModal.addEventListener('shown.bs.modal', function() {
                    if (!map) {
                        initMap();
                    }
                    setTimeout(() => map?.invalidateSize(), 100);
                });
            }
        });
});

function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

function initMap() {
    try {
        // Initialize map centered on Moscow
        map = L.map('map').setView([55.7558, 37.6173], 10);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Add search control
        const searchControl = L.Control.geocoder({
            defaultMarkGeocode: false
        }).addTo(map);

        // Handle search results
        searchControl.on('markgeocode', function(e) {
            const location = e.geocode.center;
            updateMarkerAndAddress(location);
            map.setView(location, 16);
        });

        // Handle map clicks
        map.on('click', function(e) {
            updateMarkerAndAddress(e.latlng);
        });
    } catch (error) {
        console.error('Error initializing map:', error);
    }
}

function updateMarkerAndAddress(latlng) {
    // Update or create marker
    if (marker) {
        marker.setLatLng(latlng);
    } else {
        marker = L.marker(latlng, {draggable: true}).addTo(map);
        marker.on('dragend', function() {
            reverseGeocode(marker.getLatLng());
        });
    }

    // Show additional fields and enable save button
    document.getElementById('additionalFields').style.display = 'block';
    document.getElementById('saveAddressBtn').disabled = false;

    // Get address from coordinates
    reverseGeocode(latlng);
}

function reverseGeocode(latlng) {
    fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latlng.lat}&lon=${latlng.lng}&format=json`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('addressInput').value = data.display_name;
        })
        .catch(error => console.error('Error getting address:', error));
}

function saveAddress() {
    if (!marker) {
        alert('Please select a location on the map');
        return;
    }

    const addressData = {
        address: document.getElementById('addressInput').value,
        building: document.getElementById('buildingInput').value,
        floor: document.getElementById('floorInput').value,
        apartment: document.getElementById('apartmentInput').value,
        coordinates: {
            lat: marker.getLatLng().lat,
            lng: marker.getLatLng().lng
        }
    };

    // Send address data to server
    fetch('/save_address', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(addressData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Close modal and reload page to show updated address
            const modal = bootstrap.Modal.getInstance(document.getElementById('addressModal'));
            modal.hide();
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error saving address:', error);
        alert('Error saving address. Please try again.');
    });
} 