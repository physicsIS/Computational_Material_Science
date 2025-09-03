#!/bin/bash

# Archivo de salida final
outfile="energias.dat"
> "$outfile"   # lo vacía si existe

for file in $(ls *.out | sort); do
	echo "Pasando archivo $file"
	grep "!" "$file" | awk '{print $5}' >> "$outfile"
done

echo "Energías guardadas en $outfile"