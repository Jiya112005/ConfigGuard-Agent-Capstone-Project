from deepdiff import DeepDiff

from deepdiff import DeepDiff

class DriftAgent:
    def __init__(self):
        pass

    def detect_drift(self, intended_config, actual_config):
        print("🕵️ Drift Agent: Comparing configurations...")
        
        # Calculate the difference
        diff = DeepDiff(intended_config, actual_config, ignore_order=True)
        
        # Debug: Show Raw Output
        if diff:
            print(f"🔍 DEBUG: Raw DeepDiff Output:\n{diff}")
        else:
            print("✅ Drift Agent: No raw differences found.")
            return []
        
        # Parse the difference
        return self._parse_diff_report(diff)

    def _parse_diff_report(self, diff):
        drift_summary = []
        print("🔍 DEBUG: Starting to parse report...")

        
        if 'values_changed' in diff:
            print("   -> Found 'values_changed' key in diff.") 
            for key, change in diff['values_changed'].items():
                print(f"   -> Processing key: {key}")
                path = key.replace("root", "")
                old_val = change.get('old_value', 'N/A')
                new_val = change.get('new_value', 'N/A')
                
                message = f"❌ VALUE MISMATCH at {path}: Intended '{old_val}', found '{new_val}'"
                drift_summary.append(message)

        
        if 'type_changes' in diff:
            print("   -> Found 'type_changes' key in diff.")
            for key, change in diff['type_changes'].items():
                path = key.replace("root", "")
                old_val = change.get('old_value', 'N/A')
                new_val = change.get('new_value', 'N/A')
                
                message = f"❌ TYPE MISMATCH at {path}: Intended '{old_val}', found '{new_val}'"
                drift_summary.append(message)

        
        if 'dictionary_item_added' in diff:
            print("   -> Found 'dictionary_item_added'.")
            for key in diff['dictionary_item_added']:
                drift_summary.append(f"⚠️ UNEXPECTED KEY: {key}")

        if 'dictionary_item_removed' in diff:
            print("   -> Found 'dictionary_item_removed'.")
            for key in diff['dictionary_item_removed']:
                drift_summary.append(f"⚠️ MISSING KEY: {key}")

        print(f"🔍 DEBUG: Final drift_summary list has {len(drift_summary)} items.")
        return drift_summary