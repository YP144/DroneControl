% Definisikan Parameter Sistem
tau = 0.983; % Konstanta waktu sistem 
K = 80.147  ; % Penguatan sistem
A = 1; % Kemiringan sinyal ramp

% Definisikan Sistem di Domain Laplace
s = tf('s'); % Definisikan operator Laplace
G = K / (tau * s + 1); % Fungsi transfer sistem

% Definisikan Sinyal Ramp
U = A / s^2; % Fungsi transfer sinyal ramp

% Hitung Respon Sistem
Y = G * U; % Fungsi transfer output

% Simulasi dan Plot Respon
t = 0:0.01:4; % Rentang waktu simulasi
[y, t] = impulse(Y, t); % Hitung respon terhadap sinyal ramp

% Plot hasil simulasi
plot(t, y)
title('Respon Sistem Orde 1 terhadap Sinyal Ramp')
xlabel('Waktu (detik)')
ylabel('Output y(t)')
grid on