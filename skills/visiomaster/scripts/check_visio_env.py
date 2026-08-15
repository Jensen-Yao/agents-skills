from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check whether local Microsoft Visio COM automation works.")
    parser.add_argument(
        "--output-dir",
        default="exports/compatibility_check",
        help="Directory for smoke-test outputs.",
    )
    parser.add_argument("--visible", action="store_true", help="Show Visio while running the check.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        import win32com.client.gencache as gencache
    except ImportError:
        print("[FAIL] pywin32 is not installed in this Python environment.")
        print("       Run: python -m pip install -r requirements.txt")
        return 2

    try:
        app = gencache.EnsureDispatch("Visio.Application")
    except Exception as exc:
        print("[FAIL] Could not start Microsoft Visio through COM.")
        print(f"       {exc}")
        print("       Make sure Microsoft Visio desktop is installed, licensed, and can be opened normally.")
        return 3

    app.Visible = bool(args.visible)
    doc = None
    try:
        try:
            app.AlertResponse = 7
        except Exception:
            pass

        doc = app.Documents.Add("")
        page = doc.Pages.Item(1)
        page.PageSheet.CellsU("PageWidth").FormulaU = "6 in"
        page.PageSheet.CellsU("PageHeight").FormulaU = "3 in"

        shape = page.DrawRectangle(1, 1, 3, 2)
        shape.Text = "Visiomaster"
        shape.CellsU("FillForegnd").FormulaU = "RGB(180,220,240)"
        shape.CellsU("LineColor").FormulaU = "RGB(80,80,80)"

        line = page.DrawLine(3.4, 1.5, 5.2, 1.5)
        line.CellsU("EndArrow").ResultIU = 13

        vsdx_path = output_dir / "visiomaster_compatibility_check.vsdx"
        png_path = output_dir / "visiomaster_compatibility_check.png"
        svg_path = output_dir / "visiomaster_compatibility_check.svg"

        doc.SaveAs(str(vsdx_path))
        print(f"[OK] Wrote VSDX: {vsdx_path}")

        export_failures: list[str] = []
        for export_path in (png_path, svg_path):
            try:
                page.Export(str(export_path))
                print(f"[OK] Exported: {export_path}")
            except Exception as exc:
                export_failures.append(f"{export_path.name}: {exc}")

        if export_failures:
            print("[WARN] Visio started and saved VSDX, but some exports failed:")
            for item in export_failures:
                print(f"       - {item}")
            return 1

        print("[OK] Visio COM automation is available for Visiomaster.")
        return 0
    except Exception as exc:
        print("[FAIL] Visio COM smoke test failed.")
        print(f"       {exc}")
        return 4
    finally:
        if doc is not None:
            try:
                doc.Saved = True
                doc.Close()
            except Exception:
                pass
        try:
            app.Quit()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
