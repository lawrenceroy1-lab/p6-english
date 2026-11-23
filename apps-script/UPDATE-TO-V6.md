# Update the Google Sheet code to v6 (maths + English)

The maths site keeps working exactly as now. English scores go to a new tab, "English Scores" (it is made by itself the first time a student plays).
The web app link stays the same, so nothing changes on the maths site.

1. Open your Google Sheet (the same one as maths).
2. Click **Extensions** > **Apps Script**.
3. Click inside the code, press **Cmd + A** (select all), then **Delete**.
4. Open the file `apps-script/Code.gs` from this folder, copy all of it, and paste it in.
5. Click the **💾 Save** icon.
6. Click **Deploy** > **Manage deployments**.
7. Click the **✏️ pencil** (Edit) next to your web app.
8. Under **Version**, choose **New version**. Click **Deploy**.
9. Check: open the web app link in a new tab. It should say: *T. Roy score receiver is working ✅ (code v6, maths and English)*.

Done! Do NOT click "New deployment" (that would make a new link).
