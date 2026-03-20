from app.vault_manager import VaultManager

VAULT_PATH = "local_brain/obsidian_vault"


def main():
    vault = VaultManager(VAULT_PATH)
    vault.setup_vault_structure()
    print(f"Vault structure created at: {vault.vault_path.resolve()}")


if __name__ == "__main__":
    main()