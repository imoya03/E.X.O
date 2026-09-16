namespace E.X.O_
{
    public static class Datos
    {
        public const double Gravedad = 9.81;

        // --- Valores medidos del proyecto ---
        public const double LongitudBrazo = 0.216;      // m
        public const double LongitudAntebrazo = 0.170;  // m
        public const double LongitudTotal = 0.386;       // m
        public const double MasaParteMovil = 0.427;      // kg
        public const double TorqueServoKgCm = 11.0;      // kg*cm a 6V
        public const int ServosEnHombro = 2;

        // Distancia al centro de masa, tratando la parte movil como un
        // punto ubicado a la mitad de la longitud total (caso normal).
        public static double DistanciaCentroDeMasa()
        {
            return LongitudTotal / 2.0;
        }

        // Peor caso: toda la masa concentrada en el extremo del brazo
        // (ej. sosteniendo un objeto pesado en el efector final).
        public static double DistanciaPeorCaso()
        {
            return LongitudTotal;
        }
    }
}