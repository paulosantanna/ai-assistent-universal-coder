FROM php:8.5-apache

RUN set -eux; \
    a2enmod rewrite headers expires; \
    docker-php-ext-install mysqli pdo_mysql

COPY docker/apache-wordpress.conf /etc/apache2/conf-available/wordpress.conf
RUN a2enconf wordpress

WORKDIR /var/www/html
