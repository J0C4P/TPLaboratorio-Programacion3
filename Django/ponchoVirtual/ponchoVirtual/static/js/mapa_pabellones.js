document.addEventListener("DOMContentLoaded", function () {
    const contenedor = document.getElementById("map-pabellones");
    if (!contenedor) return;

    const map = L.map("map-pabellones").setView([-28.4484, -65.7576], 18);

    L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", {
        attribution: "Tiles &copy; Esri &mdash; Poncho Digital",
        maxZoom: 20
    }).addTo(map);

    const scriptDatos = document.getElementById("datos-mapa-data");
    if (!scriptDatos) return;

    const datosMapa = JSON.parse(scriptDatos.textContent || "{}");

    const configuracionPabellones = {
        "Pabellón A: Textiles y Telar": {
            bounds: [[-28.44835, -65.75860], [-28.44775, -65.75800]],
            borde: "#1a5276",
            fondo: "#ebf5fb"
        },
        "Pabellón B: Cerámica, Madera y Metal": {
            bounds: [[-28.44745, -65.75780], [-28.44685, -65.75720]],
            borde: "#784212",
            fondo: "#fef5e7"
        },
        "Pabellón C: Gastronomía y Sabores": {
            bounds: [[-28.44970, -65.75760], [-28.44910, -65.75700]],
            borde: "#7d6608",
            fondo: "#fef9e7"
        },
        "Pabellón D: Artesanías en Cuero": {
            bounds: [[-28.44830, -65.75720], [-28.44770, -65.75660]],
            borde: "#4a235a",
            fondo: "#f4ecf7"
        }
    };

    for (const [nombrePabellon, config] of Object.entries(configuracionPabellones)) {
        const info = datosMapa[nombrePabellon] || { stands: [] };
        const stands = info.stands || [];

        // 1. Dibujar el pabellón
        const pabellonRect = L.rectangle(config.bounds, {
            color: config.borde,
            weight: 2,
            fillColor: config.fondo,
            fillOpacity: 0.65
        }).addTo(map);

        pabellonRect.bindTooltip(`<strong>${nombrePabellon}</strong>`, {
            permanent: true,
            direction: "top",
            className: "pabellon-label"
        });

        // 2. Cuadrícula de stands interiores
        const total = stands.length;
        if (total > 0) {
            const latMin = config.bounds[0][0];
            const lngMin = config.bounds[0][1];
            const latMax = config.bounds[1][0];
            const lngMax = config.bounds[1][1];

            const margenLat = (latMax - latMin) * 0.12;
            const margenLng = (lngMax - lngMin) * 0.12;
            const areaLat = (latMax - latMin) - (2 * margenLat);
            const areaLng = (lngMax - lngMin) - (2 * margenLng);

            const columnas = Math.ceil(Math.sqrt(total));
            const filas = Math.ceil(total / columnas);

            const altoStand = areaLat / filas;
            const anchoStand = areaLng / columnas;

            stands.forEach((st, idx) => {
                const fila = Math.floor(idx / columnas);
                const col = idx % columnas;

                const sLat1 = latMin + margenLat + (fila * altoStand) + (altoStand * 0.1);
                const sLat2 = sLat1 + (altoStand * 0.8);
                const sLng1 = lngMin + margenLng + (col * anchoStand) + (anchoStand * 0.1);
                const sLng2 = sLng1 + (anchoStand * 0.8);

                const colorStand = st.ocupado ? "#dc3545" : "#28a745";

                const standRect = L.rectangle([[sLat1, sLng1], [sLat2, sLng2]], {
                    color: st.ocupado ? "#900C3F" : "#196F3D",
                    weight: 1,
                    fillColor: colorStand,
                    fillOpacity: 0.85
                }).addTo(map);

                let contenido = `
                    <div style="font-family: sans-serif; font-size: 13px;">
                        <h5 style="margin: 0 0 5px 0;">Stand N° ${st.numero}</h5>
                        <p style="margin: 0 0 3px 0;"><strong>Pabellón:</strong> ${nombrePabellon.split(':')[0]}</p>
                        <p style="margin: 0 0 5px 0;"><strong>Estado:</strong> 
                            <span style="color: ${colorStand}; font-weight: bold;">${st.ocupado ? 'Ocupado' : 'Disponible'}</span>
                        </p>
                `;

                if (st.ocupado) {
                    contenido += `
                        <hr style="margin: 6px 0;">
                        <p style="margin: 0 0 3px 0;"><strong>Artesano:</strong> ${st.artesano}</p>
                        ${st.emprendimiento ? `<p style="margin: 0 0 3px 0;"><strong>Emprendimiento:</strong> ${st.emprendimiento}</p>` : ''}
                        ${st.rubro ? `<p style="margin: 0;"><strong>Rubro:</strong> ${st.rubro}</p>` : ''}
                    `;
                }

                contenido += `</div>`;
                standRect.bindPopup(contenido);
            });
        }
    }
});