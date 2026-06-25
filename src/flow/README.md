# Power Automate Flow Export

This directory contains the exported Microsoft Power Automate Cloud flow package for the ISAAI Automated Daily Report Processing system.

## Files
- `*.zip` — The exported Power Automate flow package. Place your downloaded ZIP export file directly in this folder.

## How to Import this Flow

To import this flow into your Power Automate environment:
1. Go to [make.powerautomate.com](https://make.powerautomate.com).
2. Navigate to **My flows** in the left menu.
3. Click on **Import** at the top toolbar and select **Import Package (Legacy)**.
4. Upload the `.zip` file from this folder.
5. In the **Review Package Content** screen:
   - Under **Related resources**, map the connections (Outlook/Exchange, SharePoint, Excel Online, PowerPoint Online) to your own user account connections.
6. Click **Import**.
7. Once imported, open the flow in the designer and:
   - Update the **SharePoint Site Address** and **Library/List Names** to match your target SharePoint environment.
   - Turn the flow **On** to start processing.
