# FastAPI-TelnyxSMS2Email

**A Python FastAPI program for receiving SMS messages**

Using FastAPI, the server listens for the SMS webhooks from the SIP provider Telnyx.

1. Listens for the message.received from the API.

2. Matches the "To" phone number from a csv file loaded in memory from the data directory.

3. Retrieves the email.

4. Assembles the message.

5. Emails the message.

Below the setup will walk you through cloning the github, setting up the docker-compose.yml, configuring the csv file to use the app, the caddyfile for caddy as a HTTPS reverse proxy, and testing using a powershell command to invoke a rest method.

## Setup

1.  Clone this repository: `git clone https://github.com/NetCoreType/TelnyxSMS2Email.git`, then enter the directory `cd TelnyxSMS2Email` or do a `docker pull netcoretype/fastapi-telnyxsms2email`. If you pull the container from docker hub, skip step 2.

2.  Run the command `docker build -t fastapi-telnyxsms2email .`

3.  Using a text editor to create the following docker-compose.yml file:

    ```yaml
    services:
      fastapi-telnyxsms2email:
        image: netcoretype/fastapi-telnyxsms2email:latest
        container_name: fastapi-telnyxsms2email
        hostname: fastapi-telnyxsms2email
        env_file:
          - .env
        volumes:
          - fastapi_data:/data
        networks:
          - caddy_network
        expose:
          - 8000
        restart: unless-stopped

      caddy:
        image: caddy:latest
        cap_add:
          - NET_ADMIN
        restart: unless-stopped
        ports:
          - "80:80"
          - "443:443"
          - "443:443/udp"
        volumes:
          - /opt/caddy:/etc/caddy
          - caddy_data:/data
          - caddy_config:/config
        networks:
          - caddy_network

      volumes:
      fastapi_data:
      caddy_data:
      caddy_config:

      networks:
      caddy_network:
        driver: bridge
    ```

4.  Build an environmental file with the following options and must follow if the variable is string, integer, or boolean:

    ```bash
    SMTP_PASS=<Email server password> #String Value
    SMTP_USER=<Email server sign-in> #String Value
    SMTP_HOST=<Email relay server> #String Value
    SMTP_PORT=<Port Number> #Integer value
    SMTP_FROM_ADDRESS=<Email sending address> #String Value
    PRODUCTION=<True or False> #Boolean value
    ```

    _Note if production is set to **FALSE**, the docs will be available to test with. If production is set to **TRUE** only the api is available_

5.  Using the same text editor, create a `Caddyfile` to be put in the `/etc/caddy` directory, see the example below config:

    ```bash
    {
      email admin@email.com
    }
    <FQDN> {
            reverse_proxy fastapi-telnyxsms2email:8000
    }
    ```

6.  To start the containers by running the following:

    ```bash
    docker compose up -d
    ```

7.  Edit the email_list file in the docker-named volume and add the a phone number and email address:

    ```bash
    phone_number,email_address
    +13155551234,email@email.com
    +13125000000,telnyx@email.com
    ```

8.  Everything should be up and working now, if you want to test out if it works. Running the follow powershell command will
    invoke a rest method that you will be able to see in the logs of the docker container showing the message the was received,
    and will receive an email with the test message.

        **Template modified from 'https://developers.telnyx.com/docs/messaging/messages/receive-message'**

    ```powershell
    # Define the target URL
    $uri = "https://<FQDN>/api"


    # Define the Body
    $body = @{
      data = @{
          event_type = "message.received"
          id = "4ee8c3a6-4995-4309-a3c6-38e3db9ea4be"
          occurred_at = "2019-12-09T21:32:14.148+00:00"
          payload = @{
              completed_at = "2019-12-09T21:32:14.148+00:00"
              cost = @{
                  amount = "0.0051"
                  currency = "USD"
              }
              cost_breakdown = @{
                  carrier_fee = @{
                      amount = "0.00305"
                      currency = "USD"
                  }
                  rate = @{
                      amount = "0.00205"
                      currency = "USD"
                  }
              }
              direction = "outbound"
              encoding = "GSM-7"
              errors = @()
              from = @{
                  carrier = "T-Mobile USA"
                  line_type = "Wireless"
                  phone_number = "+13125000000"
                  status = "webhook_delivered"
              }
              id = "ac012cbf-5e09-46af-a69a-7c0e2d90993c"
              media = @()
              messaging_profile_id = "83d2343b-553f-4c5f-b8c8-fd27004f94bf"
              organization_id = "9d76d591-1b7d-405d-8c64-1320ee070245"
              parts = 1
              received_at = "2019-12-09T21:32:13.552+00:00"
              record_type = "message"
              sent_at = "2019-12-09T21:32:13.596+00:00"
              tags = @("tag-a", "tag-b")
              text = "Hello there!"
              to = @(
                  @{
                      carrier = "T-MOBILE USA, INC."
                      line_type = "Wireless"
                      phone_number = "+13125000000"
                      status = "delivered"
                  }
              )
              type = "SMS"
              valid_until = "2019-12-09T22:32:13.552+00:00"
              webhook_failover_url = ""
              webhook_url = ""
              tcr_campaign_billable = $true
              tcr_campaign_id = "CNZO3VL"
              tcr_campaign_registered = "REGISTERED"
          }
          record_type = "event"
      }
      meta = @{
          attempt = 1
          delivered_to = ""
      }
    }


    ##Convert to Json
    $jsonBody = $body | ConvertTo-Json -Depth 10


    ##Invoke the RestMethod
    Invoke-RestMethod -Uri $uri -Method Post -Body $jsonBody -ContentType "application/json"
    ```

## License

MIT

## Author

This project was create in 2026 by Rob Miller.
