from app.models.base_model import Client, Advisor
from app.models.calls_model import ProcessInitiated, Call
from app.config.database import get_db
from app.config.twilio import get_client
from app.utils.json import to_dict
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists
from io import BytesIO
from twilio.twiml.voice_response import VoiceResponse
import pandas as pd
import time


class MainService():
    def __init__(self):
        self.db = next(get_db())
        self.client_twilio = get_client()
        self.resp = None

    def get_clients(self):
        return self.db.query(Client).all()
    
    def delete(self):
        self.db.query(Client).delete()
        self.db.commit()
        self.db.query(Call).delete()
        self.db.commit()
    
    def get_client_by_ssid(self, ssid):
        call = self.db.query(Call).filter_by(ssid=ssid).first()
        client = self.db.query(Client).filter_by(id=call.client_id).first()
        advisor = self.db.query(Advisor).filter_by(id=call.advisor_id).first()
        if not client:
            None, advisor
        client_dict = to_dict(client)
        return client_dict, advisor
    
    def get_stadistics(self):
        pending_calls = self.db.query(Client).filter(
            ~self.db.query(Call).filter(Call.client_id == Client.id).exists()
        ).all()
        finished = self.db.query(Call).filter_by(status="completed").all()
        data = {
            "pending_calls": len(pending_calls),
            "finished_calls": len(finished)
        }
        return data
       
    def load_xlsx(self, content):
        try:
            df = pd.read_excel(BytesIO(content))
            for _, row in df.iterrows():
                client = Client(name=row["Nombre"], document=row["Cedula"], phone_number=row["Numero"], reason=row["Razon"])
                self.db.add(client)
                self.db.commit()
            return self.get_clients()
        except Exception as e:
            return {"error": str(e)} 
        
    def export_xlsx(self):
        results = self.db.query(Call, Client).join(Client, Call.client_id == Client.id).all()
        df = pd.DataFrame()
        for call, client in results:
            df = df._append({
                "Nombre": client.name,
                "Cedula": client.document,
                "Numero": client.phone_number,
                "Razon": client.reason,
                "Estado": call.status
            }, ignore_index=True)
        buffer = BytesIO()
        df.to_excel(buffer, "clients.xlsx", index=False, engine="openpyxl")
        buffer.seek(0)
        return buffer

    def start_calls(self):
        process = self.db.query(ProcessInitiated).first()
        if not process:
            process = ProcessInitiated(started=True)
            self.db.add(process)
            self.db.commit()
            self.db.refresh(process)
        else:
            if process.started:
                return {"error": "Ya se ha iniciado el proceso"}
            process.started = True
            self.db.commit()

        clients = self.db.query(Client).all()
        for client in clients:
            while True:
                advisors = self.db.query(Advisor).filter(
                    and_(
                        Advisor.in_call==False,
                        Advisor.active==True
                        )
                    ).all()
                if not advisors:
                    time.sleep(5)
                    continue
                break
            advisor = advisors[0]
            advisor.in_call = True
            self.db.commit()
            self.resp = VoiceResponse()
            self.resp.say("Conectando con un asesor. Por favor espere.", voice="Polly.Andres-Neural", language="es-MX")
            self.resp.dial("+57" + advisor.phone_number, ringtone="mx", answer_on_bridge=True)
            self.resp.say("Adios", voice="Polly.Andres-Neural", language="es-MX")
            call = self.client_twilio.calls.create(
                to="+57"+client.phone_number,
                from_="+17753709884",
                twiml=str(self.resp),
                status_callback="https://85ae-186-180-21-42.ngrok-free.app/call-finished/",
                status_callback_event=["answered", "completed"]
            )
            call_db = Call(ssid=call.sid, client_id=client.id, advisor_id=advisor.id)
            self.db.add(call_db)
            self.db.commit()
        
        process.started = False
        self.db.commit()
        return {"message": "Llamadas terminadas"}
    
    def call_finished(self, CallSid, CallStatus):
        call = self.db.query(Call).filter_by(ssid=CallSid).first()
        call.status = CallStatus
        self.db.commit()
        advisor = self.db.query(Advisor).filter_by(id=call.advisor_id).first()
        advisor.in_call = False
        self.db.commit()
            