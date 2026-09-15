import { useState } from "react";
import { MapContainer, TileLayer, LayersControl } from "react-leaflet";
import Card from "../components/ui/Card";
import ProspectivityLayer from "../components/map/ProspectivityLayer";
import DrillHoleLayer from "../components/map/DrillHoleLayer";
import { PROSPECTIVITY_CELLS, DRILL_HOLES } from "../data/mockData";

const MOIL_BELT_CENTER: [number, number] = [21.45, 79.6];

export default function ProspectivityMap() {
  const [selectedScore, setSelectedScore] = useState<number | null>(null);

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-xl font-semibold">AI Prospectivity Map</h1>
        <p className="text-sm text-text-muted mt-1">
          Prospectivity scoring over 50m grid cells, drill-hole overlay,
          satellite-derived indicators
        </p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="col-span-3">
          <Card className="p-0 overflow-hidden">
            <div style={{ height: "620px" }}>
              <MapContainer
                center={MOIL_BELT_CENTER}
                zoom={9}
                style={{ height: "100%", width: "100%", background: "#12140F" }}
              >
                <LayersControl position="topright">
                  <LayersControl.BaseLayer checked name="Dark Basemap">
                    <TileLayer
                      url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
                      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                      className="map-tiles-dark"
                    />
                  </LayersControl.BaseLayer>
                  <LayersControl.BaseLayer name="Satellite">
                    <TileLayer
                      url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                      attribution="Tiles &copy; Esri"
                    />
                  </LayersControl.BaseLayer>

                  <LayersControl.Overlay checked name="Prospectivity Cells">
                    <ProspectivityLayer cells={PROSPECTIVITY_CELLS} />
                  </LayersControl.Overlay>
                  <LayersControl.Overlay checked name="Drill Holes">
                    <DrillHoleLayer holes={DRILL_HOLES} />
                  </LayersControl.Overlay>
                </LayersControl>
              </MapContainer>
            </div>
          </Card>
        </div>

        <div className="space-y-4">
          <Card title="Legend">
            <div className="space-y-2 text-xs font-mono">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-ore inline-block" />
                <span>High prospectivity (&gt;75%)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-geo inline-block" />
                <span>Moderate (50–75%)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-text-muted inline-block" />
                <span>Low priority (&lt;50%)</span>
              </div>
              <div className="flex items-center gap-2 pt-2 border-t border-border mt-2">
                <span className="w-2 h-2 rounded-full bg-text-primary inline-block" />
                <span>Drill hole location</span>
              </div>
            </div>
          </Card>

          <Card title="Cell Inspector">
            {selectedScore === null ? (
              <p className="text-xs text-text-muted">
                Click a prospectivity cell on the map to inspect it.
              </p>
            ) : (
              <p className="text-xs font-mono">Score: {selectedScore}%</p>
            )}
          </Card>

          <Card title="Data Category" className="border-ore/30">
            <p className="text-xs text-text-muted leading-relaxed">
              Prospectivity cells and drill holes shown here are a{" "}
              <span className="text-ore">Demonstration Synthetic Dataset</span>.
              Satellite layers are public imagery providers; no MOIL
              confidential data is used.
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
}
