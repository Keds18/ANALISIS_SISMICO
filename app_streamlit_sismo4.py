import streamlit as st                   # Pra crear paginas web
import numpy as np                       # Para operaciones matematicas
import pandas as pd                      # Para manejar datos en forma de tablas
import io                                # Para manejar archivos en memoria
import openpyxl                          # Para crear y manipular archivos Excel
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart import LineChart
from openpyxl.chart.layout import Layout
from openpyxl.chart.layout import ManualLayout
from openpyxl.drawing.line import LineProperties
from analisis_modal3 import realizar_calculos
from funcion_graficos import graficar_fuerza_cortante_real, graficar_combinaciones_modales

st.set_page_config(page_title="ANÁLISIS MODAL-ESPECTRAL", layout="wide") #Titulo navegador y diseño de la pagina en todo el ancho
st.title("🏢 ANÁLISIS MODAL-ESPECTRAL DINAMICO") #Titulo de la pagina

# Entrada de datos
try: # Bloque para manejar errores
    st.header("1.Datos:") # Encabezado para la sección de datos
    st.subheader("Número de pisos")
    num_pisos = st.slider("", min_value=1, max_value=30, value=5, step=1)
    st.subheader("Número de modos")
    num_modos = st.number_input("", min_value=1, value=3) # Entrada para el número de modos, que son las frecuencias naturales del sistema
    st.subheader("Ingrese masas por piso")
    masas_input = st.text_area("(separadas por coma)", value="31.8,31.8,31.8,31.8,27.5") # Entrada para las masas por piso
    # Convertir la entrada de masas a un array de numpy
    masas = np.array([float(x.strip()) for x in masas_input.split(",") if x.strip() != ""])

    if len(masas) != num_pisos: # Validación de la longitud de las masas
        st.error(f"El número de masas ({len(masas)}) no coincide con el número de pisos ({num_pisos}).") # Mensaje de error si no coinciden
        st.stop()

    st.subheader("Ingrese matriz de modos")
    st.markdown(" (una fila por piso, columnas separadas por coma):")
    modos_input = st.text_area(
    "Ejemplo:",
    """0.03112, -0.08102, 0.10415,
    0.05959, -0.10493, 0.03021,
    0.08302, -0.05484, -0.09525,
    0.09940, 0.03358, -0.05769,
    0.10834, 0.10609, 0.09176
    """  
    )
    modos = np.array([
        [float(val.strip()) for val in row.split(",") if val.strip() != ""]
        for row in modos_input.strip().split("\n") if row.strip() != ""
    ])

    if modos.shape != (num_pisos, num_modos):
        st.error(f"La matriz de modos debe ser de tamaño {num_pisos}x{num_modos}. Actualmente es {modos.shape}.")
        st.stop()

    st.subheader("Periodos modales")
    periodos_input = st.text_input("(separados por coma)", value="0.556,0.193,0.126")
    periodos = np.array([float(x.strip()) for x in periodos_input.split(",") if x.strip() != ""])

    if len(periodos) != num_modos:
        st.error(f"El número de periodos ({len(periodos)}) no coincide con el número de modos ({num_modos}).")
        st.stop()

    Z = st.number_input("Factor Z", value=0.45)
    U = st.number_input("Factor U", value=1.0)
    S = st.number_input("Factor S", value=1.0)
    R = st.number_input("Factor R", value=8)
    Tp = st.number_input("Tp", value=0.4)
    TL = st.number_input("TL", value=2.5)
    g = st.number_input("g (aceleración gravitacional)", value=9.81)

    st.header("2.Resultados:")  # H2_Encabezado para la sección de cargas puntuales

    if st.button("Calcular análisis modal-espectral"):
        pisos = np.arange(1, num_pisos + 1)

        pisos, F, V, Vsum_abs, Vrcsc, Vmc_h, Vreal = realizar_calculos(
            pisos, masas, modos, periodos, g, Z, U, S, R, Tp, TL
        )

        st.success("✅ Cálculos completados correctamente")

        st.subheader("Tabla: Fuerzas Cortantes Reales por Piso")
        df_resultados = pd.DataFrame({
            'Piso': pisos,
            'Vsum_abs (ton)': Vsum_abs,
            'Vrcsc (ton)': Vrcsc,
            'Vmc_h (ton)': Vmc_h,
            'Fuerza Cortante Real (ton)': Vreal,
        })
        st.dataframe(df_resultados)

        st.subheader("Gráfico: Fuerza Cortante Real por Piso")
        fig1 = graficar_fuerza_cortante_real(pisos, Vreal)
        st.pyplot(fig1)

        st.subheader("Gráfico: Combinaciones Modales")
        fig2 = graficar_combinaciones_modales(pisos, Vsum_abs, Vrcsc, Vmc_h, Vreal)
        st.pyplot(fig2)

        # Creación avanzada del reporte Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Resultados Cortantes"

        # Escribir encabezados
        headers = ['Piso', 'Vsum_abs', 'Vrcsc', 'Vmc_h', 'Vreal']
        ws.append(headers)

        # Insertar datos
        for i in range(len(pisos)):
            ws.append([pisos[i], Vsum_abs[i], Vrcsc[i], Vmc_h[i], round(Vreal[i], 2)])

        # Crear gráfico de barras
        chart_bar = BarChart()
        chart_bar.type = "bar"
        chart_bar.style = 10
        chart_bar.width = 20  # Ancho del gráfico
        chart_bar.height = 10  # Altura del gráfico
        chart_bar.title = "Cortante Real en la Base (Vreal)"
        chart_bar.y_axis.title = "Cortante (ton)"
        chart_bar.x_axis.title = "Piso"
        data = Reference(ws, min_col=5, min_row=1, max_row=len(pisos)+1)
        categorias = Reference(ws, min_col=1, min_row=2, max_row=len(pisos)+1)
        cats = Reference(ws, min_col=1, min_row=2, max_row=len(pisos)+1)
        chart_bar.add_data(data, titles_from_data=True)
        chart_bar.set_categories(cats)
        chart_bar.dataLabels = DataLabelList(showVal=True)
        ws.add_chart(chart_bar, "G7")
        chart_bar.x_axis.delete = False # Mostrar eje X 
        chart_bar.y_axis.delete = False # Mostrar eje Y

        # Crear gráfico circular (pie chart)
        chart_pie = PieChart()
        chart_pie.style = 10  # Estilo de gráfico
        chart_pie.width = 20  # Ancho del gráfico
        chart_pie.height = 10  # Altura del gráfico
        chart_pie.title = "Distribución de Vreal por Piso"
        chart_pie.add_data(data, titles_from_data=True)
        chart_pie.set_categories(cats)
        chart_pie.dataLabels = DataLabelList(showVal=True)
        ws.add_chart(chart_pie, "G29")

        # Guardar archivo en memoria
        output = io.BytesIO()
        wb.save(output)
        excel_data = output.getvalue()

        st.subheader("📥 Descargar reporte Excel con gráficos")
        st.download_button(
            label="Descargar Excel",
            data=excel_data,
            file_name='reporte_modal_espectral.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        st.success("✅ Reporte Excel preparado con éxito")

except Exception as e:
    st.error(f"⚠ Ocurrió un error durante la ejecución: {e}")
