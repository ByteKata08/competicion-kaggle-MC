"""Calcula y muestra la distribución de patrones por clase de la variable objetivo `treatment`."""

from pathlib import Path
import sys
import pandas as pd

TARGET_COLUMN = "treatment"


def calcular_distribucion(csv_path: Path) -> None:
    """Carga el CSV indicado e imprime la distribución de clases de `treatment`."""
    if not csv_path.is_file():
        print(f"Error: no se encontró el archivo '{csv_path}'.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(csv_path)

    if TARGET_COLUMN not in df.columns:
        print(
            f"Error: la columna '{TARGET_COLUMN}' no existe en '{csv_path}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    serie = df[TARGET_COLUMN]
    total_patrones = len(df)
    nulos = int(serie.isna().sum())

    conteo = serie.value_counts(dropna=False)
    porcentaje = (serie.value_counts(normalize=True, dropna=False) * 100).round(2)

    resumen = pd.DataFrame(
        {
            "Patrones": conteo,
            "Porcentaje (%)": porcentaje,
        }
    )
    resumen.index.name = TARGET_COLUMN

    print(f"Dataset: {csv_path}")
    print(f"Total de patrones: {total_patrones}")
    print(f"Valores nulos en '{TARGET_COLUMN}': {nulos}")
    print("\nDistribución de patrones por clase:")
    print(resumen.to_string())

    clases_no_nulas = serie.value_counts(dropna=True)
    if len(clases_no_nulas) >= 2:
        mayoritaria = clases_no_nulas.iloc[0]
        minoritaria = clases_no_nulas.iloc[-1]
        ratio = mayoritaria / minoritaria
        print(
            f"\nRatio de desbalanceo (mayoritaria/minoritaria): "
            f"{mayoritaria}/{minoritaria} = {ratio:.4f}"
        )


def main() -> None:
    """Punto de entrada del script."""
    default_path = Path(__file__).resolve().parent / "data" / "survey.csv"
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path
    calcular_distribucion(csv_path)


if __name__ == "__main__":
    main()
