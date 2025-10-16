async function loadBuildingData() {
  if (isLoading) return;

  const button = document.getElementById("loadData");
  const status = document.getElementById("status");

  isLoading = true;
  button.disabled = true;
  status.innerHTML = '<span class="loading">Loading building data...</span>';

  // Clear existing data
  buildingLayer.clearLayers();
  buildingStats = {};

  const bounds = getCurrentBounds();

  // Overpass API query for ALL buildings in current view
  const overpassQuery = `
    [out:json][timeout:30];
    (
        way["building"](${bounds.south}, ${bounds.west}, ${bounds.north}, ${bounds.east});
        relation["building"](${bounds.south}, ${bounds.west}, ${bounds.north}, ${bounds.east});
    );
    out geom;
 `;

  try {
    const response = await fetch("https://overpass-api.de/api/interpreter", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "data=" + encodeURIComponent(overpassQuery),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.elements.length === 0) {
      status.innerHTML =
        '<span style="color: orange;">No buildings found in this area</span>';
      updateLegend();
      updateStats();
      return;
    }

    status.textContent = `Processing ${data.elements.length} buildings...`;

    data.elements.forEach((element) => {
      if (element.type === "way" && element.geometry) {
        // Get building type, default to 'unspecified' if not present
        let buildingType = element.tags.building || "unspecified";

        // If building tag is just "yes", try to get more specific type from other tags
        if (buildingType === "yes") {
          if (element.tags.amenity) {
            buildingType = element.tags.amenity;
          } else if (element.tags.shop) {
            buildingType = "shop";
          } else if (element.tags.office) {
            buildingType = "office";
          } else if (element.tags.leisure) {
            buildingType = element.tags.leisure;
          } else {
            buildingType = "yes"; // Keep as generic building
          }
        }

        // Count building types
        buildingStats[buildingType] = (buildingStats[buildingType] || 0) + 1;

        // Convert coordinates to Leaflet format
        const coordinates = element.geometry.map((coord) => [
          coord.lat,
          coord.lon,
        ]);

        // Create popup content with all available information
        let popupContent = `<strong>Building Type:</strong> ${buildingType}<br>`;
        if (element.tags.name)
          popupContent += `<strong>Name:</strong> ${element.tags.name}<br>`;
        if (element.tags["addr:street"])
          popupContent += `<strong>Street:</strong> ${element.tags["addr:street"]}<br>`;
        if (element.tags["addr:housenumber"])
          popupContent += `<strong>Number:</strong> ${element.tags["addr:housenumber"]}<br>`;
        if (element.tags["addr:postcode"])
          popupContent += `<strong>Postcode:</strong> ${element.tags["addr:postcode"]}<br>`;
        if (element.tags.amenity)
          popupContent += `<strong>Amenity:</strong> ${element.tags.amenity}<br>`;
        if (element.tags.shop)
          popupContent += `<strong>Shop:</strong> ${element.tags.shop}<br>`;
        if (element.tags.office)
          popupContent += `<strong>Office:</strong> ${element.tags.office}<br>`;
        if (element.tags.leisure)
          popupContent += `<strong>Leisure:</strong> ${element.tags.leisure}<br>`;
        if (element.tags.levels)
          popupContent += `<strong>Levels:</strong> ${element.tags.levels}<br>`;

        // Create polygon with higher opacity for unspecified buildings
        const fillOpacity = buildingType === "unspecified" ? 0.3 : 0.6;
        const polygon = L.polygon(coordinates, {
          color: getBuildingColor(buildingType),
          fillColor: getBuildingColor(buildingType),
          fillOpacity: fillOpacity,
          weight: 1,
          opacity: 0.8,
        }).bindPopup(popupContent);

        buildingLayer.addLayer(polygon);
      }
    });

    updateLegend();
    updateStats();

    const totalBuildings = Object.values(buildingStats).reduce(
      (sum, count) => sum + count,
      0
    );
    status.innerHTML = `<span style="color: green;">Loaded ${totalBuildings} buildings</span>`;
  } catch (error) {
    console.error("Error loading data:", error);
    status.innerHTML = `<span style="color: red;">Error: ${error.message}</span>`;
  } finally {
    isLoading = false;
    button.disabled = false;
  }
}
