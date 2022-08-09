FROM ubuntu:20.04

LABEL maintainer="Seb"

COPY resources /

RUN apt-get update \
        && apt-get install -y --no-install-recommends \
        xvfb \
        supervisor \
        x11vnc \
        fluxbox

WORKDIR /tmp/

ADD https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb .

RUN apt install -y /tmp/google-chrome*.deb

RUN apt-get clean

RUN apt-get clean \
        && rm -rf /var/cache/* /var/log/apt/* /var/lib/apt/lists/* /tmp/* \
        && useradd -m chrome \
        && usermod -s /bin/bash chrome \
        && mkdir -p /home/chrome/.fluxbox \
        && mkdir -p /home/chrome/.config \
        && echo ' \n\
                session.screen0.toolbar.visible:        false\n\
                session.screen0.fullMaximization:       true\n\
                session.screen0.maxDisableResize:       true\n\
                session.screen0.maxDisableMove: true\n\
                session.screen0.defaultDeco:    NONE\n\
        ' >> /home/chrome/.fluxbox/init \
        && chown -R chrome:chrome /home/chrome/.config /home/chrome/.fluxbox

VOLUME ["/home/chrome"]

EXPOSE 5900

USER chrome

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
