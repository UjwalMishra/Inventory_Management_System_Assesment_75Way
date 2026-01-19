from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.realtime.alert_manager import alert_manager
from app.services.report_service import get_low_stock_report

router = APIRouter()


# WebSocket connection (like Pusher channel)
@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await alert_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        alert_manager.disconnect(websocket)


# Manual trigger to push alerts (VERY IMPORTANT)
@router.post("/alerts/trigger")
async def trigger_low_stock_alerts(
    session: Session = Depends(get_session),
):
    alerts = get_low_stock_report(session)

    for alert in alerts:
        await alert_manager.broadcast({
            "type": "LOW_STOCK",
            **alert,
        })

    return {"message": "Low stock alerts pushed successfully"}
