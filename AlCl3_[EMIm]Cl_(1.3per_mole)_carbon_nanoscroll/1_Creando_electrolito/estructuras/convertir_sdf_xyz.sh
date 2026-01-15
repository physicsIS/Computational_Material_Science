mkdir -p xyz  # Crear la carpeta xyz si no existe

# Recorrer todos los archivos .sdf en la carpeta originales
for file in originales/*.sdf; do
    # Verificar si se encontraron archivos
    if [ -f "$file" ]; then
        echo "Convirtiendo: $file"
        
        # Eliminar la extensión .sdf y agregar .xyz
        base_name=$(basename "$file" .sdf)
        
        # Usar Open Babel para convertir el archivo
        obabel "$file" -O "xyz/$base_name.xyz"
    else
        echo "No se encontraron archivos .sdf en la carpeta 'originales'."
    fi
done

