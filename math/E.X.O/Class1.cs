using E.X.O_;

namespace E.X.O_
{
    public static class Calculos
    {
        // 1 kgf*cm = 0.0981 N*m
        public static double KgCmANm(double kgCm)
        {
            return kgCm * Datos.Gravedad * 0.01;
        }

        public static double PesoTotal()
        {
            return Datos.MasaParteMovil * Datos.Gravedad;
        }

        // Momento requerido: M = W * d
        public static double Momento(double peso, double distancia)
        {
            return peso * distancia;
        }

        // Momento que debe aportar cada servo: M / n
        public static double MomentoPorServo(double momentoTotal, int cantidadServos)
        {
            return momentoTotal / cantidadServos;
        }

        // Torque disponible sumando todos los servos del eje
        public static double TorqueDisponible(double torqueServoKgCm, int cantidadServos)
        {
            return KgCmANm(torqueServoKgCm) * cantidadServos;
        }

        // Factor de seguridad: FS = M_disponible / M_requerido
        public static double FactorSeguridad(double torqueDisponible, double momentoRequerido)
        {
            if (momentoRequerido <= 0)
            {
                return 0;
            }
            return torqueDisponible / momentoRequerido;
        }
    }
}