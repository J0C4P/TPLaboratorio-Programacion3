document.addEventListener("DOMContentLoaded", function () {
    // 1. Inicializar el mapa sobre el Predio Ferial con zoom 18
    var map = L.map('mapaPredio').setView([-28.4483, -65.7573], 18);

    // 2. Capa base de Esri
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19,
        attribution: 'Tiles &copy; Esri &mdash; Poncho Digital'
    }).addTo(map);

    // 3. Leer los datos enviados por Django
    var rawData = document.getElementById('datos-mapa-data');
    var datos = {};
    if (rawData && rawData.textContent) {
        try {
            datos = JSON.parse(rawData.textContent);
        } catch (e) {
            console.error("Error al leer datos:", e);
        }
    }

    // 4. Renderizar cada pabellón como un edificio con su grilla de stands
    for (var nombrePabellon in datos) {
        if (!datos.hasOwnProperty(nombrePabellon)) continue;
        var info = datos[nombrePabellon];
        if (!info.lat || !info.lng) continue;

        var standsLista = info.stands || [];
        var totalStands = standsLista.length;
        var ocupados = 0;
        for (var i = 0; i < standsLista.length; i++) {
            if (standsLista[i].ocupado) ocupados++;
        }
        var libres = totalStands - ocupados;

        var nombreCorto = nombrePabellon.split(":")[0]; // "Pabellón A", "Pabellón B", etc.

        // Construir los cuadritos chicos para cada stand
        var cuadritosHtml = '';
        if (standsLista.length === 0) {
            cuadritosHtml = '<div style="font-size: 10px; color: #6c757d; padding: 6px; text-align: center; grid-column: span 3;">Sin stands asignados</div>';
        } else {
            for (var j = 0; j < standsLista.length; j++) {
                var st = standsLista[j];
                var claseColor = st.ocupado ? 'stand-cuadro-ocupado' : 'stand-cuadro-libre';
                var tituloHover = st.ocupado 
                    ? 'Stand #' + st.numero + ' (Ocupado: ' + (st.artesano || '') + ')' 
                    : 'Stand #' + st.numero + ' (Disponible)';

                cuadritosHtml += '' +
                    '<div class="stand-cuadro ' + claseColor + '" title="' + tituloHover + '">' +
                        '<span class="stand-num">#' + st.numero + '</span>' +
                    '</div>';
            }
        }

        // Estructura completa del pabellón arquitectónico
        var iconoHtml = '' +
            '<div class="pabellon-edificio shadow">' +
                '<div class="pabellon-techo">' +
                    '<span class="pabellon-titulo">' + nombreCorto + '</span>' +
                    '<span class="pabellon-resumen">' + libres + 'L / ' + ocupados + 'O</span>' +
                '</div>' +
                '<div class="pabellon-planta">' +
                    cuadritosHtml +
                '</div>' +
            '</div>';

        // Creamos el divIcon personalizado sin el globo azul
        var pabellonIcon = L.divIcon({
            className: 'custom-pabellon-marker',
            html: iconoHtml,
            iconSize: [170, 'auto'],
            iconAnchor: [85, 45]
        });

        var marker = L.marker([info.lat, info.lng], { icon: pabellonIcon }).addTo(map);

        // POPUP detallado con lista y datos del artesano al hacer clic en el pabellón
        var popupHtml = '' +
            '<div style="min-width: 270px; max-height: 290px; overflow-y: auto; font-family: sans-serif;">' +
            '<h6 style="margin: 0 0 4px 0; font-weight: bold; color: #8B4513;">' + nombrePabellon + '</h6>' +
            '<div style="font-size: 12px; margin-bottom: 8px;">' +
                '<span style="color: #0e9f6e; font-weight: bold;">Libres: ' + libres + '</span> | ' +
                '<span style="color: #e02424; font-weight: bold;">Ocupados: ' + ocupados + '</span> (Total: ' + totalStands + ')' +
            '</div>' +
            '<hr style="margin: 4px 0 8px 0;">' +
            '<div style="display: flex; flex-direction: column; gap: 6px;">';

        for (var k = 0; k < standsLista.length; k++) {
            var item = standsLista[k];
            if (item.ocupado) {
                popupHtml += '' +
                    '<div style="background: #fde8e8; border: 1px solid #f8b4b4; border-radius: 6px; padding: 6px; font-size: 11px;">' +
                        '<div style="display: flex; justify-content: space-between; align-items: center;">' +
                            '<strong>Stand #' + item.numero + '</strong>' +
                            '<span style="color: #c81e1e; font-weight: bold; font-size: 10px;">OCUPADO</span>' +
                        '</div>' +
                        '<div style="margin-top: 3px;"><b>Artesano:</b> ' + (item.artesano || 'Asignado') + '</div>' +
                        '<div><b>Emprendimiento:</b> ' + (item.emprendimiento || 'Sin taller registrado') + '</div>' +
                        (item.rubro ? '<div style="color: #666; font-style: italic;">Rubro: ' + item.rubro + '</div>' : '') +
                    '</div>';
            } else {
                popupHtml += '' +
                    '<div style="background: #def7ec; border: 1px solid #bcf0da; border-radius: 6px; padding: 6px; font-size: 11px; display: flex; justify-content: space-between; align-items: center;">' +
                        '<strong>Stand #' + item.numero + '</strong>' +
                        '<span style="color: #0e9f6e; font-weight: bold; font-size: 10px;">DISPONIBLE</span>' +
                    '</div>';
            }
        }

        popupHtml += '</div></div>';
        marker.bindPopup(popupHtml);
    }
});