disp("yes")
%% 

v = 0.1;
% Fungsi gain berdasarkan kecepatan
K = @(v) 937.34 * v + 0.8953;

% Konstanta waktu
tau = 1.2396;

% Buat model sistem orde 1
sys = @(v) tf(K(v), [tau 1]);

% Setpoint atau referensi yang diinginkan
r = 1; % Misalnya, ingin robot bergerak dari y=0 ke y=1

% Parameter PID (tuning)
Kp = 1.0;
Ki = 0.5;
Kd = 0.2;

% Buat objek PID controller
C = pid(Kp, Ki, Kd);

% Sistem kontrol tertutup
T = @(v) feedback(C * sys(v), 1);

% Waktu simulasi
t = 0:0.01:10; % Misalnya simulasi dari 0 hingga 10 detik

% Kecepatan robot (misalnya, bisa bervariasi)
v = 1.0; % Contoh: kecepatan robot 1 m/s

% Respon sistem terhadap referensi
[y, t] = step(r * T(v), t); % Respon sistem terhadap setpoint r

% Plot hasil simulasi
figure;
plot(t, y, 'b', 'LineWidth', 2);
grid on;
xlabel('Time (seconds)');
ylabel('Position (y)');
title('PID Control Simulation');

%% 
% Impor gambar drone
drone_icon = imread("drone.png");

% Tentukan skala ukuran gambar (sesuaikan dengan ukuran yang diinginkan)
icon_size = 100; % Ukuran gambar dalam pixel
imshow(drone_icon);

%% 

% Contoh data posisi x dan waktu t
x = [0 0.2 0.5 0.8 1.2 1.5 1.7 1.9 2.1];
t = [0 1 2 3 4 5 6 7 8]; % Waktu yang sesuai dengan posisi x

figure;
axis([-1 3 min(x)-0.5 max(x)+0.5]); % Sesuaikan batas sumbu x dan y sesuai kebutuhan
grid on;
xlabel('Time');
ylabel('Position (x)');
title('Robot Movement Animation');

% Loop untuk animasi
for i = 1:length(t)
    plot(t(1:i), x(1:i), 'b', 'LineWidth', 2); % Plot data yang sudah diperbarui
    hold on;
    plot(t(i), x(i), 'ro', 'MarkerSize', 10); % Plot titik posisi saat ini sebagai lingkaran merah
    hold off;
    pause(0.1); % Jeda antara setiap frame animasi
end


%% 

t1 = 0:0.01:2;
t2 = (2+0.01):0.01:4;
t3 = (4+0.01):0.01:6;
t4 = (6+0.01):0.01:8;
t = [t1,t2,t3,t4];
u1 =[];
for i = 1:length(t1)
    u1 = [u1,0.05];
end
u2 =[];
for i = 1:length(t2)
    u2 = [u2,0.1];
end
u3 =[];
for i = 1:length(t3)
    u3 = [u3,0.15];
end
u4 =[];
for i = 1:length(t4)
    u4 = [u4,0.2];
end
u = [u1,u2,u3,u4];
figure(1);
plot(t,u);
grid on;
hold on;

y0 = 450;
tfl = 0;
y=[y0];
umin1 = 0;
x = [200];
for i = 2:length(t)

    if (u(i) ~= umin1)
        tfl = t(i);
        y0 = y(end);
        y = [y,y0];
    elseif (u(i) == umin1)
        y = [y,y0+sistemX("mundur", u(i), t(i)-tfl)];
    end
    umin1 = u(i);
    x = [x,200];
end

plot(t,y);

% Impor gambar drone
[drone_icon, ~, alpha] = imread('quadrotor.png');

% Tentukan skala ukuran gambar (sesuaikan dengan ukuran yang diinginkan)
icon_size = 60; % Ukuran gambar dalam pixel

figure(2);

xlabel('Time');
ylabel('Position (x)');

% Loop untuk animasi
for i = 1:length(t)
    figure(2);
    plot(x(1:i), y(1:i), 'b', 'LineWidth', 2); % Plot data yang sudah diperbarui
    axis([0 400 0 500]); % Sesuaikan batas sumbu x dan y sesuai kebutuhan
    grid on;
    hold on;
    % plot(x(i), y(i), 'ro', 'MarkerSize', 10); % Plot titik posisi saat ini sebagai lingkaran merah
    % Tampilkan gambar drone sebagai simbol titik posisi saat ini
    h = image(x(i), y(i), drone_icon, 'XData', [x(i)-icon_size/2 x(i)+icon_size/2], 'YData', [y(i)-icon_size/2 y(i)+icon_size/2]);
    % Atur AlphaData untuk menetapkan transparansi
    set(h, 'AlphaData', alpha);
    hold off;
    pause(0.01); % Jeda antara setiap frame animasi
end

% Definisi fungsi dalam script
function y = sistemX(arah, kec, t)
    if arah == "maju"
        if kec ~= 0
            gainMaju = 937.34 * kec + 0.8953;
        elseif kec == 0
            gainMaju = 0;
        end
        tauMaju = 1.2396;
        s = tf('s'); % Definisikan operator Laplace
        Gmaju = gainMaju / (tauMaju * s + 1); % Fungsi transfer sistem
        U = 1 / s^2; % Fungsi transfer sinyal ramp
        Ymaju = Gmaju * U; % Fungsi transfer output
        Ystep = s * Gmaju * U;
        % Simulasi dan Plot Respon
        outsim = step(Ystep, t); % Hitung respon terhadap sinyal ramp
        y = outsim(end);

    elseif arah == "mundur"
        if kec ~= 0
            gainMundur = -1*(1242.79 * kec - 4.531);
        elseif kec == 0
            gainMundur = 0;
        end
        
        tauMundur = 1.949;
        s = tf('s'); % Definisikan operator Laplace
        Gmundur = gainMundur / (tauMundur * s + 1); % Fungsi transfer sistem
        U = 1 / s^2; % Fungsi transfer sinyal ramp
        Ymundur = Gmundur * U; % Fungsi transfer output
        Ystep = s * Gmundur * U;
        % Simulasi dan Plot Respon
        outsim = step(Ystep, t); % Hitung respon terhadap sinyal ramp
        y = outsim(end);
    end
end



