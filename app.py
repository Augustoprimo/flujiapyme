import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai
from datetime import datetime
import os

st.set_page_config(page_title="FinIA PyME", page_icon="📊", layout="wide")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def ia(prompt):
    r = model.generate_content(prompt)
    return r.text

def fp(n):
    return f"${n:,.0f}".replace(",",".")

def cp():
    return dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#c8d0e7",
        xaxis=dict(gridcolor="#2a3a55", linecolor="#2a3a55"),
        yaxis=dict(gridcolor="#2a3a55", linecolor="#2a3a55")
    )

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:#0f1117;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a1f2e,#131720);border-right:1px solid #2a3044;}
section[data-testid="stSidebar"] *{color:#c8d0e7!important;}
.app-header{background:linear-gradient(135deg,#1e2d4a,#0d1a2e);border:1px solid #2a4a7a;border-radius:16px;padding:28px 36px;margin-bottom:24px;}
.app-header h1{font-family:'Space Grotesk',sans-serif;color:#e8f0ff;font-size:1.9rem;font-weight:700;margin:0 0 6px 0;}
.app-header p{color:#7a90b8;font-size:0.9rem;margin:0;}
.badge{display:inline-block;background:rgba(56,139,253,0.15);border:1px solid rgba(56,139,253,0.4);color:#388bfd;font-size:0.7rem;font-weight:700;padding:3px 10px;border-radius:20px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px;}
.mc{background:#1a2035;border:1px solid #2a3a55;border-radius:12px;padding:18px 20px;position:relative;overflow:hidden;margin-bottom:8px;}
.mc::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;}
.mc.b::after{background:linear-gradient(90deg,#1f6feb,#388bfd);}
.mc.g::after{background:linear-gradient(90deg,#2ea043,#56d364);}
.mc.o::after{background:linear-gradient(90deg,#d29922,#e3b341);}
.mc.r::after{background:linear-gradient(90deg,#b91c1c,#ef4444);}
.mc.p::after{background:linear-gradient(90deg,#6f42c1,#a78bfa);}
.ml{color:#7a90b8;font-size:0.72rem;font-weight:500;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;}
.mv{color:#e8f0ff;font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;line-height:1;}
.ms{color:#4d6080;font-size:0.75rem;margin-top:4px;}
.st2{color:#c8d0e7;font-family:'Space Grotesk',sans-serif;font-size:1.05rem;font-weight:600;margin:24px 0 14px;padding-bottom:7px;border-bottom:1px solid #2a3a55;}
.ia-box{background:linear-gradient(135deg,#1a2540,#141e35);border:1px solid #2a4a7a;border-left:3px solid #388bfd;border-radius:10px;padding:18px 20px;margin-top:14px;color:#c8d0e7;line-height:1.7;font-size:0.9rem;}
.ia-lbl{font-size:0.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#388bfd;margin-bottom:8px;display:block;}
.aw{background:rgba(210,153,34,.1);border:1px solid rgba(210,153,34,.3);border-radius:8px;padding:11px 15px;color:#e3b341;font-size:0.85rem;margin:7px 0;}
.ad{background:rgba(185,28,28,.1);border:1px solid rgba(185,28,28,.3);border-radius:8px;padding:11px 15px;color:#ef4444;font-size:0.85rem;margin:7px 0;}
.ok{background:rgba(46,160,67,.1);border:1px solid rgba(46,160,67,.3);border-radius:8px;padding:11px 15px;color:#56d364;font-size:0.85rem;margin:7px 0;}
.cu{background:#1f2d44;border:1px solid #2a3a55;border-radius:10px 10px 2px 10px;padding:10px 14px;color:#e8f0ff;margin:6px 0 3px auto;max-width:80%;float:right;clear:both;font-size:0.88rem;}
.ca{background:#1a2035;border:1px solid #2a4a7a;border-radius:10px 10px 10px 2px;padding:10px 14px;color:#c8d0e7;margin:3px auto 6px 0;max-width:85%;float:left;clear:both;font-size:0.88rem;line-height:1.6;}
.stTabs [data-baseweb="tab-list"]{background:#1a2035;border-radius:8px;padding:4px;gap:4px;}
.stTabs [data-baseweb="tab"]{color:#7a90b8!important;border-radius:6px!important;font-weight:500!important;}
.stTabs [aria-selected="true"]{background:#1f6feb!important;color:white!important;}
.stNumberInput input,.stTextInput input,.stTextArea textarea{background:#1a2035!important;border:1px solid #2a3a55!important;color:#e8f0ff!important;border-radius:8px!important;}
label{color:#7a90b8!important;font-size:0.83rem!important;}
.stButton>button{background:linear-gradient(135deg,#1f6feb,#388bfd)!important;color:white!important;border:none!important;border-radius:8px!important;font-weight:600!important;padding:9px 20px!important;}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:20px 0 22px;'>
        <div style='font-size:2rem;'>📊</div>
        <div style='font-family:Space Grotesk,sans-serif;font-size:1.1rem;font-weight:700;color:#e8f0ff;margin-top:6px;'>FinIA PyME</div>
        <div style='font-size:0.72rem;color:#4d6080;margin-top:3px;'>Asistente Financiero con IA</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    pag = st.radio("Nav", ["🏠  Inicio","📥  Ingresar Datos","📊  Análisis Financiero",
                            "📋  Control Presupuestario","🤖  Asistente IA","📄  Generar Informe"],
                   label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:0.7rem;color:#4d6080;text-align:center;'>Trabajo Final · IA Aplicada<br>Augusto Primo · UCA Rosario</div>", unsafe_allow_html=True)

pag = pag.split("  ")[1]

if "D" not in st.session_state:
    st.session_state.D = {
        "empresa":"Distribuidora Comercial Rosario SRL","periodo":"Enero 2026",
        "ventas":12000000,"costo_ventas":7200000,"gastos_admin":2500000,
        "gastos_com":1200000,"pres_ventas":13000000,"pres_costos":7000000,
        "pres_admin":2200000,"pres_com":1100000,"hist":[],"chat":[],
    }
D = st.session_state.D

if pag == "Inicio":
    st.markdown("""<div class='app-header'>
        <div class='badge'>✦ IA Aplicada al Análisis Financiero</div>
        <h1>Asistente de Gestión Financiera para PyMEs</h1>
        <p>Análisis inteligente · Control presupuestario · Reportes automáticos</p>
    </div>""", unsafe_allow_html=True)
    gb = D["ventas"]-D["costo_ventas"]
    rop = gb-D["gastos_admin"]-D["gastos_com"]
    mop = rop/D["ventas"]*100 if D["ventas"] else 0
    rco = D["costo_ventas"]/D["ventas"]*100 if D["ventas"] else 0
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        st.markdown(f"<div class='mc b'><div class='ml'>Ventas Totales</div><div class='mv'>{fp(D['ventas'])}</div><div class='ms'>{D['periodo']}</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='mc o'><div class='ml'>Costo de Ventas</div><div class='mv'>{fp(D['costo_ventas'])}</div><div class='ms'>{rco:.1f}% de ventas</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='mc p'><div class='ml'>Ganancia Bruta</div><div class='mv'>{fp(gb)}</div><div class='ms'>Margen {gb/D['ventas']*100:.1f}%</div></div>", unsafe_allow_html=True)
    with c4:
        cls = "g" if rop > 0 else "r"
        st.markdown(f"<div class='mc {cls}'><div class='ml'>Resultado Op.</div><div class='mv'>{fp(rop)}</div><div class='ms'>Margen {mop:.1f}%</div></div>", unsafe_allow_html=True)
    with c5:
        gt = D["gastos_admin"]+D["gastos_com"]
        st.markdown(f"<div class='mc r'><div class='ml'>Total Gastos</div><div class='mv'>{fp(gt)}</div><div class='ms'>{gt/D['ventas']*100:.1f}% de ventas</div></div>", unsafe_allow_html=True)
    cg,cd = st.columns(2)
    with cg:
        st.markdown('<div class="st2">Estructura de Resultados</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute","relative","relative","relative","total"],
            x=["Ventas","- Costo","- G.Admin","- G.Com","Resultado"],
            y=[D["ventas"],-D["costo_ventas"],-D["gastos_admin"],-D["gastos_com"],0],
            connector={"line":{"color":"#2a3a55"}},
            increasing={"marker":{"color":"#2ea043"}},
            decreasing={"marker":{"color":"#ef4444"}},
            totals={"marker":{"color":"#388bfd"}},
            text=[fp(D["ventas"]),fp(-D["costo_ventas"]),fp(-D["gastos_admin"]),fp(-D["gastos_com"]),fp(rop)],
            textposition="outside"
        ))
        fig.update_layout(**cp(), height=300, margin=dict(t=10,b=10,l=0,r=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with cd:
        st.markdown('<div class="st2">Distribución de Egresos</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=["Costo Ventas","G. Admin","G. Comerciales","Resultado"],
            values=[D["costo_ventas"],D["gastos_admin"],D["gastos_com"],max(rop,0)],
            hole=0.55,
            marker=dict(colors=["#ef4444","#d29922","#a78bfa","#2ea043"],line=dict(color="#0f1117",width=2)),
            textinfo="label+percent",textfont=dict(color="#c8d0e7",size=11)
        ))
        fig2.update_layout(**cp(), height=300, margin=dict(t=10,b=10,l=0,r=0), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

elif pag == "Ingresar Datos":
    st.markdown("""<div class='app-header'>
        <div class='badge'>📥 Datos de la Empresa</div>
        <h1>Ingreso de Información Financiera</h1>
        <p>Completá los datos del período para habilitar el análisis completo</p>
    </div>""", unsafe_allow_html=True)
    with st.form("fd"):
        c1,c2 = st.columns(2)
        with c1:
            emp = st.text_input("Nombre de la empresa", value=D["empresa"])
        with c2:
            per = st.text_input("Período analizado", value=D["periodo"])
        st.markdown('<div class="st2">Estado de Resultados Real</div>', unsafe_allow_html=True)
        r1,r2 = st.columns(2)
        with r1:
            v = st.number_input("Ventas totales ($)", min_value=0, value=D["ventas"], step=100000, format="%d")
            ga = st.number_input("Gastos administrativos ($)", min_value=0, value=D["gastos_admin"], step=50000, format="%d")
        with r2:
            cv = st.number_input("Costo de ventas ($)", min_value=0, value=D["costo_ventas"], step=100000, format="%d")
            gc = st.number_input("Gastos comerciales ($)", min_value=0, value=D["gastos_com"], step=50000, format="%d")
        st.markdown('<div class="st2">Presupuesto Planificado</div>', unsafe_allow_html=True)
        p1,p2 = st.columns(2)
        with p1:
            pv = st.number_input("Ventas presupuestadas ($)", min_value=0, value=D["pres_ventas"], step=100000, format="%d")
            pa = st.number_input("G. admin presupuestados ($)", min_value=0, value=D["pres_admin"], step=50000, format="%d")
        with p2:
            pc = st.number_input("Costos presupuestados ($)", min_value=0, value=D["pres_costos"], step=100000, format="%d")
            pgc = st.number_input("G. comerciales presupuestados ($)", min_value=0, value=D["pres_com"], step=50000, format="%d")
        ok = st.form_submit_button("💾  Guardar datos")
    if ok:
        hist = D["hist"].copy()
        hist.append({"periodo":D["periodo"],"ventas":D["ventas"],"rop":D["ventas"]-D["costo_ventas"]-D["gastos_admin"]-D["gastos_com"]})
        st.session_state.D.update({"empresa":emp,"periodo":per,"ventas":v,"costo_ventas":cv,
            "gastos_admin":ga,"gastos_com":gc,"pres_ventas":pv,"pres_costos":pc,"pres_admin":pa,"pres_com":pgc,"hist":hist[-6:]})
        st.markdown('<div class="ok">✅ Datos guardados correctamente.</div>', unsafe_allow_html=True)
        D = st.session_state.D
    rop = D["ventas"]-D["costo_ventas"]-D["gastos_admin"]-D["gastos_com"]
    st.markdown('<div class="st2">Vista Previa</div>', unsafe_allow_html=True)
    df = pd.DataFrame({
        "Concepto":["Ventas","Costo de Ventas","Ganancia Bruta","G. Admin","G. Comerciales","Resultado Operativo"],
        "Importe":[fp(D["ventas"]),fp(-D["costo_ventas"]),fp(D["ventas"]-D["costo_ventas"]),fp(-D["gastos_admin"]),fp(-D["gastos_com"]),fp(rop)]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

elif pag == "Análisis Financiero":
    st.markdown("""<div class='app-header'>
        <div class='badge'>📊 Indicadores Financieros</div>
        <h1>Análisis Financiero</h1>
        <p>Ratios clave, gráficos y diagnóstico inteligente con IA</p>
    </div>""", unsafe_allow_html=True)
    gb = D["ventas"]-D["costo_ventas"]
    rop = gb-D["gastos_admin"]-D["gastos_com"]
    mb = gb/D["ventas"]*100 if D["ventas"] else 0
    mo = rop/D["ventas"]*100 if D["ventas"] else 0
    rc = D["costo_ventas"]/D["ventas"]*100 if D["ventas"] else 0
    rg = (D["gastos_admin"]+D["gastos_com"])/D["ventas"]*100 if D["ventas"] else 0
    t1,t2,t3 = st.tabs(["📐 Ratios","📈 Gráficos","🤖 Diagnóstico IA"])
    with t1:
        st.markdown('<div class="st2">Indicadores Clave</div>', unsafe_allow_html=True)
        for nom,val,ref,ok in [
            ("Margen Bruto",f"{mb:.2f}%",">30% saludable",mb>30),
            ("Margen Operativo",f"{mo:.2f}%",">10% aceptable para PyME",mo>10),
            ("Ratio Costo/Ventas",f"{rc:.2f}%","<60% recomendado",rc<60),
            ("Ratio Gastos/Ventas",f"{rg:.2f}%","<30% recomendado",rg<30),
            ("Resultado Operativo",fp(rop),"Debe ser positivo",rop>0)
        ]:
            ic = "✅" if ok else "⚠️"
            st.markdown(f"<div class='mc b' style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'><div><div class='ml'>{nom}</div><div class='mv' style='font-size:1.2rem;'>{val}</div><div class='ms'>{ref}</div></div><div style='font-size:1.6rem;'>{ic}</div></div>", unsafe_allow_html=True)
    with t2:
        ca,cb = st.columns(2)
        with ca:
            fig = go.Figure(go.Bar(
                x=["Ventas","G. Bruta","Res. Op."],
                y=[D["ventas"],gb,rop],
                marker_color=["#388bfd","#2ea043","#56d364" if rop>0 else "#ef4444"],
                text=[fp(v) for v in [D["ventas"],gb,rop]],
                textposition="outside",textfont=dict(color="#c8d0e7",size=10)
            ))
            fig.update_layout(**cp(),height=300,title=dict(text="Cascada de Resultados",font=dict(color="#c8d0e7")),margin=dict(t=40,b=10,l=0,r=0),showlegend=False)
            st.plotly_chart(fig,use_container_width=True)
        with cb:
            fig2 = go.Figure(go.Bar(
                x=["Margen Bruto","Margen Operativo"],
                y=[mb,mo],
                marker_color=["#d29922","#388bfd"],
                text=[f"{v:.1f}%" for v in [mb,mo]],
                textposition="outside",textfont=dict(color="#c8d0e7",size=12)
            ))
            fig2.add_hline(y=30,line_dash="dot",line_color="#56d364",annotation_text="Ref. 30%",annotation_font_color="#56d364")
            fig2.add_hline(y=10,line_dash="dot",line_color="#388bfd",annotation_text="Ref. 10%",annotation_font_color="#388bfd")
            fig2.update_layout(**cp(),height=300,title=dict(text="Márgenes (%)",font=dict(color="#c8d0e7")),margin=dict(t=40,b=10,l=0,r=0),showlegend=False)
            st.plotly_chart(fig2,use_container_width=True)
    with t3:
        if st.button("🤖 Generar Diagnóstico con IA"):
            with st.spinner("Analizando..."):
                resp = ia(f"Sos contador experto en PyMEs argentinas. Analizá {D['empresa']} para {D['periodo']}: Ventas {fp(D['ventas'])}, Costo {fp(D['costo_ventas'])} ({rc:.1f}%), G.Admin {fp(D['gastos_admin'])}, G.Com {fp(D['gastos_com'])}, G.Bruta {fp(gb)} ({mb:.1f}%), Res.Op {fp(rop)} ({mo:.1f}%). Da: 1)Diagnostico 2)Riesgos max 3 3)Recomendaciones max 3 4)Conclusion. Contexto inflacion Argentina.")
                st.markdown(f'<div class="ia-box"><span class="ia-lbl">🤖 Diagnóstico IA</span>{resp.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

elif pag == "Control Presupuestario":
    st.markdown("""<div class='app-header'>
        <div class='badge'>📋 Presupuesto vs. Real</div>
        <h1>Control Presupuestario</h1>
        <p>Comparación entre lo planificado y lo ejecutado</p>
    </div>""", unsafe_allow_html=True)
    items = [
        ("Ventas",D["ventas"],D["pres_ventas"],True),
        ("Costo de Ventas",D["costo_ventas"],D["pres_costos"],False),
        ("G. Admin",D["gastos_admin"],D["pres_admin"],False),
        ("G. Comerciales",D["gastos_com"],D["pres_com"],False)
    ]
    rr = D["ventas"]-D["costo_ventas"]-D["gastos_admin"]-D["gastos_com"]
    rp = D["pres_ventas"]-D["pres_costos"]-D["pres_admin"]-D["pres_com"]
    t1,t2,t3 = st.tabs(["📊 Tabla de Desvíos","📈 Gráfico Comparativo","🤖 Análisis IA"])
    with t1:
        rows = []
        for n,r,p,pos in items:
            dev = r-p
            devp = (dev/p*100) if p else 0
            fav = (dev>0)==pos
            rows.append({"Concepto":n,"Presupuestado":fp(p),"Real":fp(r),"Desvío $":fp(dev),"Desvío %":f"{devp:+.1f}%",
                "Estado":"✅ Favorable" if fav else ("⚠️ Atención" if abs(devp)<15 else "❌ Desfavorable")})
        devr = rr-rp
        rows.append({"Concepto":"Resultado Operativo","Presupuestado":fp(rp),"Real":fp(rr),"Desvío $":fp(devr),
            "Desvío %":f"{(devr/rp*100 if rp else 0):+.1f}%","Estado":"✅ Favorable" if devr>=0 else "❌ Desfavorable"})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        for n,r,p,pos in items:
            devp = (r-p)/p*100 if p else 0
            fav = (devp>0)==pos
            if not fav and abs(devp)>=15:
                st.markdown(f'<div class="ad">❌ <b>{n}</b>: desvío {devp:+.1f}% — acción inmediata.</div>', unsafe_allow_html=True)
            elif not fav and abs(devp)>=5:
                st.markdown(f'<div class="aw">⚠️ <b>{n}</b>: desvío {devp:+.1f}% — monitorear.</div>', unsafe_allow_html=True)
    with t2:
        cats = [n for n,*_ in items]
        rs = [D["ventas"],D["costo_ventas"],D["gastos_admin"],D["gastos_com"]]
        ps = [D["pres_ventas"],D["pres_costos"],D["pres_admin"],D["pres_com"]]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Presupuestado",x=cats,y=ps,marker_color="#388bfd",opacity=0.7))
        fig.add_trace(go.Bar(name="Real",x=cats,y=rs,marker_color="#2ea043"))
        fig.update_layout(**cp(),barmode="group",height=320,title=dict(text="Real vs. Presupuestado",font=dict(color="#c8d0e7")),margin=dict(t=40,b=10,l=0,r=0),legend=dict(font=dict(color="#c8d0e7")))
        st.plotly_chart(fig,use_container_width=True)
    with t3:
        if st.button("🤖 Analizar Desvíos con IA"):
            with st.spinner("Analizando desvíos..."):
                dtxt = "\n".join([f"- {n}: real {fp(r)}, pres {fp(p)}, desvio {((r-p)/p*100 if p else 0):+.1f}%" for n,r,p,_ in items])
                resp = ia(f"Sos controller financiero experto en PyMEs argentinas. Analiza desvios de {D['empresa']} ({D['periodo']}):\n{dtxt}\nRes.real {fp(rr)}, Pres {fp(rp)}, Desvio {fp(rr-rp)}. Da causas y 3 acciones correctivas para inflacion argentina.")
                st.markdown(f'<div class="ia-box"><span class="ia-lbl">🤖 Análisis desvíos</span>{resp.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

elif pag == "Asistente IA":
    st.markdown("""<div class='app-header'>
        <div class='badge'>🤖 Chat con IA</div>
        <h1>Asistente Financiero Inteligente</h1>
        <p>Consultá cualquier duda sobre tu situación financiera</p>
    </div>""", unsafe_allow_html=True)
    rop = D["ventas"]-D["costo_ventas"]-D["gastos_admin"]-D["gastos_com"]
    ctx = f"Empresa: {D['empresa']} ({D['periodo']}). Ventas {fp(D['ventas'])}, Costo {fp(D['costo_ventas'])}, G.Admin {fp(D['gastos_admin'])}, G.Com {fp(D['gastos_com'])}, Res.Op {fp(rop)}. PyME argentina, inflacion alta."
    st.markdown('<div class="st2">Preguntas Frecuentes</div>', unsafe_allow_html=True)
    sugs = ["Cuales son los principales riesgos?","Como reducir costos operativos?",
            "Cual es mi punto de equilibrio?","Que indicadores monitorear mensualmente?"]
    cols = st.columns(4)
    for i,s in enumerate(sugs):
        with cols[i]:
            if st.button(s,key=f"s{i}"):
                D["chat"].append({"r":"u","m":s})
                historial = "\n".join([f"{'Usuario' if m['r']=='u' else 'Asistente'}: {m['m']}" for m in D["chat"]])
                resp = ia(f"Sos asesor financiero PyMEs argentinas. Contexto:\n{ctx}\n\nConversacion:\n{historial}\n\nResponde la ultima pregunta clara y concisa.")
                D["chat"].append({"r":"a","m":resp})
    if D["chat"]:
        st.markdown('<div class="st2">Conversación</div>', unsafe_allow_html=True)
        for m in D["chat"]:
            if m["r"]=="u":
                st.markdown(f'<div style="overflow:hidden"><div class="cu">👤 {m["m"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="overflow:hidden"><div class="ca">🤖 {m["m"].replace(chr(10),"<br>")}</div></div>', unsafe_allow_html=True)
    st.markdown("")
    with st.form("cf",clear_on_submit=True):
        cx,cy = st.columns([5,1])
        with cx:
            umsg = st.text_input("Pregunta...",placeholder="Ej: Como mejoro mi rentabilidad?",label_visibility="collapsed")
        with cy:
            send = st.form_submit_button("Enviar")
    if send and umsg:
        D["chat"].append({"r":"u","m":umsg})
        historial = "\n".join([f"{'Usuario' if m['r']=='u' else 'Asistente'}: {m['m']}" for m in D["chat"]])
        resp = ia(f"Sos asesor financiero PyMEs argentinas. Contexto:\n{ctx}\n\nConversacion:\n{historial}\n\nResponde la ultima pregunta.")
        D["chat"].append({"r":"a","m":resp})
        st.rerun()
    if D["chat"] and st.button("Limpiar"):
        D["chat"] = []
        st.rerun()

elif pag == "Generar Informe":
    st.markdown("""<div class='app-header'>
        <div class='badge'>📄 Informe Automático</div>
        <h1>Diagnóstico Financiero Completo</h1>
        <p>Informe ejecutivo generado por IA</p>
    </div>""", unsafe_allow_html=True)
    gb = D["ventas"]-D["costo_ventas"]
    rop = gb-D["gastos_admin"]-D["gastos_com"]
    mb = gb/D["ventas"]*100 if D["ventas"] else 0
    mo = rop/D["ventas"]*100 if D["ventas"] else 0
    rp = D["pres_ventas"]-D["pres_costos"]-D["pres_admin"]-D["pres_com"]
    if st.button("📄 Generar Informe Completo con IA",use_container_width=True):
        with st.spinner("Generando informe ejecutivo..."):
            inf = ia(f"Sos contador senior en PyMEs argentinas. Informe ejecutivo para {D['empresa']}, {D['periodo']}. Ventas {fp(D['ventas'])}, Costo {fp(D['costo_ventas'])}, G.Admin {fp(D['gastos_admin'])}, G.Com {fp(D['gastos_com'])}, G.Bruta {fp(gb)} ({mb:.1f}%), Res.Op {fp(rop)} ({mo:.1f}%). Pres {fp(rp)}, real {fp(rop)}, desvio {fp(rop-rp)}. Incluye: 1)RESUMEN EJECUTIVO 2)ANALISIS DE RESULTADOS 3)RIESGOS 4)CONTROL PRESUPUESTARIO 5)RECOMENDACIONES 6)CONCLUSION.")
            st.session_state["inf"] = inf
    if "inf" in st.session_state:
        inf = st.session_state["inf"]
        st.markdown(f"""<div style='background:linear-gradient(135deg,#1a2540,#141e35);border:1px solid #2a4a7a;border-radius:16px;padding:26px 30px;margin:18px 0;'>
            <div style='font-family:Space Grotesk,sans-serif;font-size:1.4rem;font-weight:700;color:#e8f0ff;margin-bottom:6px;'>Diagnóstico Financiero</div>
            <div style='color:#388bfd;font-size:0.82rem;margin-bottom:18px;'>{D["empresa"]} — {D["periodo"]}</div>
            <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:20px;'>
                <div style='background:rgba(56,139,253,.08);border:1px solid rgba(56,139,253,.2);border-radius:8px;padding:12px;'>
                    <div style='color:#7a90b8;font-size:0.7rem;text-transform:uppercase;'>Ventas</div>
                    <div style='color:#e8f0ff;font-size:1.15rem;font-weight:700;'>{fp(D["ventas"])}</div></div>
                <div style='background:rgba(46,160,67,.08);border:1px solid rgba(46,160,67,.2);border-radius:8px;padding:12px;'>
                    <div style='color:#7a90b8;font-size:0.7rem;text-transform:uppercase;'>Resultado Op.</div>
                    <div style='color:#56d364;font-size:1.15rem;font-weight:700;'>{fp(rop)}</div></div>
                <div style='background:rgba(167,139,250,.08);border:1px solid rgba(167,139,250,.2);border-radius:8px;padding:12px;'>
                    <div style='color:#7a90b8;font-size:0.7rem;text-transform:uppercase;'>Margen Op.</div>
                    <div style='color:#a78bfa;font-size:1.15rem;font-weight:700;'>{mo:.1f}%</div></div>
            </div>
            <div class='ia-box' style='margin:0;'><span class='ia-lbl'>📄 Informe generado por IA</span>{inf.replace(chr(10),"<br>")}</div>
        </div>""", unsafe_allow_html=True)
        st.download_button("⬇️ Descargar informe (.txt)",
            data=f"DIAGNOSTICO FINANCIERO\n{D['empresa']} - {D['periodo']}\nGenerado: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n{'='*60}\n\n{inf}",
            file_name="informe_financiero.txt", mime="text/plain")
