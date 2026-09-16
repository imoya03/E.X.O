using E.X.O_;
using System;

namespace E.X.O_
{
    class Program
    {
        static void Main()
        {
            Console.Title = "E.X.O. - Analisis Estatico";

            MostrarBanner();

            bool salir = false;

            while (!salir)
            {
                MostrarMenu();
                string opcion = Console.ReadLine();
                Console.WriteLine();

                if (opcion == "1")
                {
                    MostrarDatos();
                }
                else if (opcion == "2")
                {
                    AnalizarCaso("CASO 1: MASA EN EL CENTRO DE MASA", Datos.DistanciaCentroDeMasa());
                }
                else if (opcion == "3")
                {
                    AnalizarCaso("CASO 2: PEOR CASO (MASA EN EL EXTREMO)", Datos.DistanciaPeorCaso());
                }
                else if (opcion == "4")
                {
                    ReporteCompleto();
                }
                else if (opcion == "0")
                {
                    salir = true;
                    EscribirColor("Hasta luego. E.X.O. se apaga.", ConsoleColor.Cyan);
                }
                else
                {
                    EscribirColor("Opcion invalida.", ConsoleColor.Red);
                }

                if (!salir)
                {
                    Console.WriteLine();
                    EscribirColor("Presione Enter para continuar...", ConsoleColor.DarkGray);
                    Console.ReadLine();
                }
            }

            Console.ResetColor();
        }

        // ==============================================================
        //  Interfaz: banner, menu y helpers de color
        // ==============================================================

        static void EscribirColor(string texto, ConsoleColor color)
        {
            Console.ForegroundColor = color;
            Console.WriteLine(texto);
            Console.ResetColor();
        }

        static void Linea(char c, int largo, ConsoleColor color)
        {
            Console.ForegroundColor = color;
            Console.WriteLine(new string(c, largo));
            Console.ResetColor();
        }

        static void Titulo(string texto)
        {
            Console.WriteLine();
            Linea('=', 60, ConsoleColor.DarkCyan);
            EscribirColor("  " + texto.ToUpper(), ConsoleColor.Cyan);
            Linea('=', 60, ConsoleColor.DarkCyan);
        }

        static void Paso(string numero, string texto)
        {
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.Write(" PASO " + numero + ": ");
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine(texto);
            Console.ResetColor();
        }

        static void MostrarBanner()
        {
            string[] letraE =
            {
                "#######",
                "#      ",
                "#####  ",
                "#      ",
                "#######"
            };
            string[] punto =
            {
                "   ",
                "   ",
                "   ",
                "   ",
                " # "
            };
            string[] letraX =
            {
                "#     #",
                " #   # ",
                "   #   ",
                " #   # ",
                "#     #"
            };
            string[] letraO =
            {
                " ##### ",
                "#     #",
                "#     #",
                "#     #",
                " ##### "
            };

            ConsoleColor[] colores = new ConsoleColor[]
            {
                ConsoleColor.Cyan,
                ConsoleColor.White,
                ConsoleColor.Yellow,
                ConsoleColor.White,
                ConsoleColor.Green
            };

            Console.WriteLine();
            for (int fila = 0; fila < 5; fila++)
            {
                Console.ForegroundColor = colores[0];
                Console.Write(letraE[fila] + " ");
                Console.ForegroundColor = colores[1];
                Console.Write(punto[fila] + " ");
                Console.ForegroundColor = colores[2];
                Console.Write(letraX[fila] + " ");
                Console.ForegroundColor = colores[3];
                Console.Write(punto[fila] + " ");
                Console.ForegroundColor = colores[4];
                Console.Write(letraO[fila]);
                Console.WriteLine();
            }
            Console.ResetColor();

            Console.WriteLine();
            EscribirColor("        EMG Extendida a Ortosis", ConsoleColor.DarkCyan);
            EscribirColor("  TMT1002.2 - Ingenieria Mecanica II - Proyecto Final", ConsoleColor.DarkGray);
            EscribirColor("  Memoria de calculo: analisis estatico del brazo robotico", ConsoleColor.DarkGray);
            Linea('=', 60, ConsoleColor.DarkCyan);
        }

        static void MostrarMenu()
        {
            Console.WriteLine();
            Linea('-', 60, ConsoleColor.DarkGray);
            EscribirColor(" MENU PRINCIPAL", ConsoleColor.Magenta);
            Linea('-', 60, ConsoleColor.DarkGray);

            Opcion("1", "Ver datos de entrada");
            Opcion("2", "Caso 1: masa en el centro de masa (d = L/2)");
            Opcion("3", "Caso 2: peor caso, masa en el extremo (d = L)");
            Opcion("4", "Reporte completo (ambos casos)");
            Opcion("0", "Salir");

            Console.ResetColor();
            Console.Write("\nOpcion: ");
        }

        static void Opcion(string numero, string texto)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write("  " + numero + ". ");
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine(texto);
        }

        // ==============================================================
        //  Logica del programa
        // ==============================================================

        static void MostrarDatos()
        {
            Titulo("1. Datos de entrada");

            Console.WriteLine("Longitud del brazo (hombro-codo): " + Datos.LongitudBrazo + " m");
            Console.WriteLine("Longitud del antebrazo (codo-efector): " + Datos.LongitudAntebrazo + " m");
            Console.WriteLine("Longitud total: " + Datos.LongitudTotal + " m");
            Console.WriteLine("Masa medida de la parte movil: " + Datos.MasaParteMovil + " kg");
            Console.WriteLine("Torque de cada servo MG996R: " + Datos.TorqueServoKgCm + " kg*cm a 6V");
            Console.WriteLine("Servos en el hombro: " + Datos.ServosEnHombro);

            Console.WriteLine();
            double peso = Calculos.PesoTotal();
            Console.WriteLine("Peso total, W = m*g = " + peso.ToString("F4") + " N");
            Console.WriteLine("Distancia centro de masa, d = L/2 = " + Datos.DistanciaCentroDeMasa().ToString("F3") + " m");
            Console.WriteLine("Distancia peor caso, d = L = " + Datos.DistanciaPeorCaso().ToString("F3") + " m");
        }

        static void AnalizarCaso(string titulo, double distancia)
        {
            Titulo(titulo);

            Paso("1", "Peso de la parte movil, W = m*g");
            double peso = Calculos.PesoTotal();
            Console.WriteLine("W = " + Datos.MasaParteMovil + " x " + Datos.Gravedad + " = " + peso.ToString("F4") + " N");

            Console.WriteLine();
            Paso("2", "Distancia al punto de aplicacion del peso, d");
            Console.WriteLine("d = " + distancia.ToString("F3") + " m");

            Console.WriteLine();
            Paso("3", "Momento requerido, M = W * d");
            double momento = Calculos.Momento(peso, distancia);
            Console.WriteLine("M = " + peso.ToString("F4") + " x " + distancia.ToString("F3") + " = " + momento.ToString("F4") + " N*m");

            Console.WriteLine();
            Paso("4", "Repartir el momento entre los " + Datos.ServosEnHombro + " servos del hombro");
            double momentoPorServo = Calculos.MomentoPorServo(momento, Datos.ServosEnHombro);
            Console.WriteLine("M_servo = M / " + Datos.ServosEnHombro + " = " + momentoPorServo.ToString("F4") + " N*m");

            Console.WriteLine();
            Paso("5", "Torque disponible (hoja de datos del MG996R)");
            double torqueServoNm = Calculos.KgCmANm(Datos.TorqueServoKgCm);
            double torqueDisponible = Calculos.TorqueDisponible(Datos.TorqueServoKgCm, Datos.ServosEnHombro);
            Console.WriteLine("1 servo = " + Datos.TorqueServoKgCm + " kg*cm = " + torqueServoNm.ToString("F4") + " N*m");
            Console.WriteLine("Torque disponible total = " + torqueServoNm.ToString("F4") + " x " + Datos.ServosEnHombro + " = " + torqueDisponible.ToString("F4") + " N*m");

            Console.WriteLine();
            Paso("6", "Factor de seguridad, FS = M_disponible / M_requerido");
            double fs = Calculos.FactorSeguridad(torqueDisponible, momento);

            Console.Write("FS = " + torqueDisponible.ToString("F4") + " / " + momento.ToString("F4") + " = ");
            if (fs >= 1.0)
            {
                EscribirColor(fs.ToString("F2"), ConsoleColor.Green);
            }
            else
            {
                EscribirColor(fs.ToString("F2"), ConsoleColor.Red);
            }

            Console.WriteLine();
            if (fs >= 1.0)
            {
                EscribirColor("RESULTADO: los servos SI soportan la carga en este caso.", ConsoleColor.Green);
            }
            else
            {
                EscribirColor("RESULTADO: los servos NO soportan la carga en este caso.", ConsoleColor.Red);
            }
        }

        static void ReporteCompleto()
        {
            MostrarDatos();
            Console.WriteLine();
            AnalizarCaso("CASO 1: MASA EN EL CENTRO DE MASA", Datos.DistanciaCentroDeMasa());
            Console.WriteLine();
            AnalizarCaso("CASO 2: PEOR CASO (MASA EN EL EXTREMO)", Datos.DistanciaPeorCaso());

            Console.WriteLine();
            Titulo("Fin del reporte");
            EscribirColor("El caso 1 representa el uso normal del brazo (masa distribuida).", ConsoleColor.DarkGray);
            EscribirColor("El caso 2 es el escenario mas conservador para el diseno.", ConsoleColor.DarkGray);
        }
    }
}