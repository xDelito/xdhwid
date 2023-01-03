import os
import sys
import subprocess

def show_banner():
  print("'::......::.:::::::::..::.....::.::.......::..::::..::::::::..")  
  print("'##::::'##:'########::'##::::'##:'##:::::'##:'####:'########::")
  print(". ##::'##:: ##.... ##: ##:::: ##: ##:'##: ##:. ##:: ##.... ##:")
  print(":. ##'##::: ##:::: ##: ##:::: ##: ##: ##: ##:: ##:: ##:::: ##:")
  print("::. ###:::: ##:::: ##: #########: ##: ##: ##:: ##:: ##:::: ##:")
  print(":: ## ##::: ##:::: ##: ##.... ##: ##: ##: ##:: ##:: ##:::: ##:")
  print(": ##:. ##:: ##:::: ##: ##:::: ##: ##: ##: ##:: ##:: ##:::: ##:")
  print(" ##:::. ##: ########:: ##:::: ##:. ###. ###::'####: ########::")
  print("..:::::..::........:::..:::::..:::...::...:::....::........:::")

show_banner()

hwid_changes = [  ("CPU", "12345678-1234-1234-1234-1234567890AB"),  ("Motherboard", "12345678-1234-1234-1234-1234567890AC"),  ("Graphics Card", "12345678-1234-1234-1234-1234567890AD")]

def change_hwid(hardware, new_hwid):
  subprocess.run(["wmic", "csproduct", "where", "name='{}'".format(hardware), "set", "UUID='{}'".format(new_hwid)])

def get_current_hwid(hardware):
  result = subprocess.run(["wmic", "csproduct", "where", "name='{}'".format(hardware), "get", "UUID"], stdout=subprocess.PIPE)
  hwid = str(result.stdout).strip()
  print("HWID actual de {}: {}".format(hardware, hwid))

def backup_hwid():
  desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
  backup_folder = os.path.join(desktop_path, 'HWID Backup')
  if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)
  for hw, _ in hwid_changes:
    result = subprocess.run(["wmic", "csproduct", "where", "name='{}'".format(hw), "get", "UUID"], stdout=subprocess.PIPE)
    hwid = str(result.stdout).strip()
    with open(os.path.join(backup_folder, hw + ".txt"), "w") as f:
      f.write(hwid)

def restore_hwid():
  desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
  backup_folder = os.path.join(desktop_path, 'HWID Backup')
  if not os.path.exists(backup_folder):
    print("No se ha encontrado ninguna copia de seguridad.")
  else:
    for hw, _ in hwid_changes:
        with open(os.path.join(backup_folder, hw + ".txt"), "r") as f:
            hwid = f.read()
            change_hwid(hw, hwid)
            
def main():
  try:
    print("Selecciona una opción:")
    print("1) Ver HWID actual")
    print("2) Realizar copia de seguridad del HWID actual")
    print("3) Restaurar HWID a partir de la copia de seguridad")
    print("4) Realizar cambios de HWID")
    print("5) Cancelar")
    option = input("Opción: ")

    if option == "1":  
      hardware = input("Selecciona una pieza de hardware (CPU, Motherboard, Graphics Card): ")
      if hardware in ["CPU", "Motherboard", "Graphics Card"]:
        get_current_hwid(hardware)
      else:
        print("Opción inválida.")
    elif option == "2":
      backup_hwid()
    elif option == "3":
      restore_hwid()
    elif option == "4":
      hardware = input("Selecciona una pieza de hardware (CPU, Motherboard, Graphics Card): ")
      if hardware in ["CPU", "Motherboard", "Graphics Card"]:
        for hw, new_hwid in hwid_changes:
          if hw == hardware:
            change_hwid(hw, new_hwid)
      else:
        print("Opción inválida.")
    elif option == "5":
      print("Cancelando...")
    else:
      print("Opción inválida.")
  except KeyboardInterrupt:
    print("\nFinalizando aplicación...")

if __name__ == "__main__":
  main()
