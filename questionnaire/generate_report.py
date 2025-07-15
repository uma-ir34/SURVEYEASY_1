import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def ensure_image_input(image_data):
    """
    Makes sure the image input is BytesIO or file path.
    If given base64, convert to BytesIO.
    """
    if isinstance(image_data, str):
        if image_data.strip().startswith("iVBOR"):  # Looks like raw Base64 PNG
            image_data = base64.b64decode(image_data)
            return io.BytesIO(image_data)
        elif image_data.strip().startswith("/"):
            return image_data  # file path
        else:
            raise ValueError("Unknown string input for image.")
    elif isinstance(image_data, bytes):
        return io.BytesIO(image_data)
    elif hasattr(image_data, 'read'):
        return image_data  # already BytesIO
    else:
        return None


def generate_pdf_report(
    title,
    result_text,
    preds_table_html,
    cm_image=None,
    balance_image=None,
    scatter_image=None,
    date_image=None,
    group_summary=None,
    model_type=None,
    survey_name=None,
    num_participants=None,
    df=None
):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    if 'CustomCode' not in styles.byName:
        styles.add(ParagraphStyle(name='CustomCode', fontName='Courier', fontSize=8))

    flowables = []

    flowables.append(Paragraph(f"<b>{title}</b>", styles['Title']))
    flowables.append(Spacer(1, 12))

    if model_type:
        flowables.append(Paragraph(f"<b>Model Type:</b> {model_type}", styles['Normal']))
    if survey_name:
        flowables.append(Paragraph(f"<b>Survey:</b> {survey_name}", styles['Normal']))
    if num_participants:
        flowables.append(Paragraph(f"<b>Participants:</b> {num_participants}", styles['Normal']))

    flowables.append(Spacer(1, 12))

    flowables.append(Paragraph(result_text.replace("\n", "<br/>"), styles['Normal']))
    flowables.append(Spacer(1, 12))

    if group_summary:
        flowables.append(Paragraph(f"<b>Group Summary:</b><br/>{group_summary.replace(chr(10), '<br/>')}", styles['Normal']))
        flowables.append(Spacer(1, 12))

    # ✅ Classification plots
    for img in [cm_image, balance_image, scatter_image, date_image]:
        img_fixed = ensure_image_input(img)
        if img_fixed:
            flowables.append(Image(img_fixed, width=400, height=300))
            flowables.append(Spacer(1, 12))

    # ✅ Correlation & question plots
    if df is not None:
        personal_cols = ['name', 'email', 'location', 'age']
        survey_cols = [c for c in df.columns if c not in personal_cols]

        if survey_cols:
            numeric_cols = df[survey_cols].select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                plt.figure(figsize=(8, 6))
                sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
                heatmap_buf = io.BytesIO()
                plt.tight_layout()
                plt.savefig(heatmap_buf, format='png')
                plt.close()
                heatmap_buf.seek(0)
                flowables.append(Paragraph("<b>Correlation Heatmap:</b>", styles['Normal']))
                flowables.append(Image(heatmap_buf, width=400, height=300))
                flowables.append(Spacer(1, 12))

            for col in survey_cols:
                plt.figure(figsize=(6, 4))
                if df[col].dtype == 'object' or df[col].nunique() < 10:
                    df[col].value_counts().plot(kind='pie', autopct='%1.1f%%')
                else:
                    df[col].value_counts().plot(kind='bar')
                plt.title(col)
                col_buf = io.BytesIO()
                plt.tight_layout()
                plt.savefig(col_buf, format='png')
                plt.close()
                col_buf.seek(0)
                flowables.append(Paragraph(f"<b>Column:</b> {col}", styles['Normal']))
                flowables.append(Image(col_buf, width=400, height=300))
                flowables.append(Spacer(1, 12))

    doc.build(flowables)
    buffer.seek(0)
    return buffer
