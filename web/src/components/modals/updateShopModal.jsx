import React, { useState, useEffect } from "react";
import { useIntl, FormattedMessage } from "react-intl";
import { v4 as uuidv4 } from "uuid";
import { format } from "date-fns";
import { Store } from "lucide-react";
import { useForm } from "react-hook-form";
import { Modal } from "./modal";
import handleFetch from "../handleFetch";

export default function UpdateShopModal({
  UpdateModalOpen,
  UpdateModalSetOpen,
  fetchShops,
  shop,
}) {
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
    reset,
  } = useForm({
    defaultValues: {
      name: shop.name,
      company_id: shop.company.id,
      location_id: shop.location.id,
    },
  });
  const [locations, setLocations] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [responseMessage, setResponseMessage] = useState("");
  const [isErrorMessage, setIsErrorMessage] = useState(false);
  const [companySwitch, setCompanySwitch] = useState(true);
  const [locationSwitch, setLocationSwitch] = useState(true);

  const intl = useIntl();
  const env_path = process.env.REACT_APP_API_PATH;

  const shopNamePlaceholder = intl.formatMessage({
    id: "addShopModal.shopNamePlaceholder",
    defaultMessage: "Shop Name",
  });
  const shopNameRequired = intl.formatMessage({
    id: "addShopModal.shopNameRequired",
    defaultMessage: "Name of the shop required",
  });
  const selectCompany = intl.formatMessage({
    id: "addShopModal.selectCompany",
    defaultMessage: "SelectCompany",
  });
  const createCompany = intl.formatMessage({
    id: "addShopModal.createCompany",
    defaultMessage: "Create Company",
  });
  const selectLocation = intl.formatMessage({
    id: "addShopModal.selectLocation",
    defaultMessage: "SelectLocation",
  });
  const createLocation = intl.formatMessage({
    id: "addShopModal.createLocation",
    defaultMessage: "Create Location",
  });
  const submit = intl.formatMessage({
    id: "updateShopModal.submit",
    defaultMessage: "Update a Shop",
  });

  // Fetch locations and companies
  useEffect(() => {
    const fetchLocationsAndCompanies = async () => {
      try {
        const locationResponse = await handleFetch(`${env_path}/location`);
        const companyResponse = await handleFetch(`${env_path}/company`);

        if (locationResponse && companyResponse) {
          setLocations(locationResponse);
          setCompanies(companyResponse);
        }
      } catch (error) {
        console.error("Error fetching locations and companies:", error);
      }
    };

    fetchLocationsAndCompanies();
  }, []);

  // POST
  const onPostSubmit = async (data) => {
    try {
      // Check if company switch is on
      if (!companySwitch) {
        const newCompanyResponse = await handleFetch(`${env_path}/company`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: data.company_name,
            description: data.company_description,
          }),
        });

        if (!newCompanyResponse) {
          setResponseMessage(newCompanyResponse.message);
          setIsErrorMessage(false);
        } else {
          data.company_id = newCompanyResponse.company_id;
        }
      }

      // Check if location switch is on
      if (!locationSwitch) {
        const newLocationResponse = await handleFetch(`${env_path}/location`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            address: data.location_address,
            zip_code: data.location_zip,
            city: data.location_city,
            country: data.location_country,
          }),
        });

        if (!newLocationResponse) {
          setResponseMessage(newLocationResponse.message);
          setIsErrorMessage(false);
        } else {
          data.location_id = newLocationResponse.location_id;
        }
      }

      // PUT request for updating shop
      const response = await handleFetch(`${env_path}/shop/${shop.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: data.name,
          company_id: data.company_id,
          location_id: data.location_id,
        }),
      });

      const newShop = await response;

      if (!response) {
        setResponseMessage(newShop.message);
        setIsErrorMessage(false);
      } else {
        setResponseMessage(newShop.message);
        setIsErrorMessage(true);
        fetchShops();
        reset();
      }
    } catch (error) {
      console.error("An error occurred:", error);
      setResponseMessage("An error occurred, please contact a dev.");
      setIsErrorMessage(true);
    }
  };
  return (
    <Modal open={UpdateModalOpen} onClose={UpdateModalSetOpen}>
      <div className="text-center mt-5 w-full ">
        <Store size={40} className="mx-auto text-AshinBlue" />
        <p
          className={` my-2 font-medium ${
            isErrorMessage ? "text-green-500" : "text-red-500"
          }`}
        >
          {responseMessage}
        </p>

        <form
          onSubmit={handleSubmit(onPostSubmit)}
          className="flex flex-col gap-4 w-96 mx-auto mt-4"
        >
          {/* Shop Name Selection  */}
          <input
            type="text"
            placeholder={shopNamePlaceholder}
            {...register("name", {
              required: shopNameRequired,
            })}
            className="p-2 border border-gray-300 rounded focus:outline-none focus:border-AshinBlue transition"
          />
          {errors.name && <p className="text-red-500">{errors.name.message}</p>}

          {/* Company Selection */}
          <ToggleSwitch
            leftLabel={selectCompany}
            rightLabel={createCompany}
            itemSwitch={companySwitch}
            setItemSwitch={setCompanySwitch}
          />
          {companySwitch
            ? CompanySelect(register, errors, companies, shop.location.id)
            : CompanyForm(register, errors)}

          {/* location Selection */}
          <ToggleSwitch
            leftLabel={selectLocation}
            rightLabel={createLocation}
            itemSwitch={locationSwitch}
            setItemSwitch={setLocationSwitch}
          />
          {locationSwitch
            ? LocationSelect(register, errors, locations, shop.company.id)
            : LocationForm(register, errors)}

          {/* Submit Selection */}
          <input
            type="submit"
            value={submit}
            className="bg-AshinBlue text-white px-4 py-2 rounded hover:opacity-90 transition"
          />
        </form>
      </div>
    </Modal>
  );
}

function CompanySelect(register, errors, companies, defaultValueCompany) {
  return (
    <>
      <select
        id="company_id"
        {...register("company_id", { required: true })}
        defaultValue={defaultValueCompany}
        className="p-2 border border-gray-300 rounded focus:outline-none focus:border-AshinBlue transition"
      >
        <option value="">
          {" "}
          <FormattedMessage
            id="addShopModal.selectCompany"
            defaultMessage="Select a Company :"
          />
        </option>
        {/* For SELECT * FROM COMPANIES */}
        {companies.map((company) => (
          <option
            key={company.id}
            value={company.id}
            selected={company.id === defaultValueCompany ? true : false}
          >
            {company.name}
          </option>
        ))}
      </select>
      {errors.company_id && (
        <span className="text-red-500 mt-1">
          <FormattedMessage
            id="addShopModal.selectCompany"
            defaultMessage="Select a Company"
          />
        </span>
      )}
    </>
  );
}

function LocationSelect(register, errors, locations, defaultValueLocation) {
  return (
    <>
      <select
        id="location_id"
        {...register("location_id", { required: true })}
        defaultValue={defaultValueLocation}
        className="p-2 border border-gray-300 rounded focus:outline-none focus:border-AshinBlue transition"
      >
        <option value="">
          {" "}
          <FormattedMessage
            id="addShopModal.selectLocation"
            defaultMessage="Select a Location :"
          />
        </option>
        {/* For SELECT * FROM locations */}
        {locations.map((location) => (
          <option
            key={location.id}
            value={location.id}
            selected={location.id === defaultValueLocation ? true : false}
          >
            {location.address}, {location.zip_code}, {location.city},{" "}
            {location.country}
          </option>
        ))}
      </select>
      {errors.location_id && (
        <span className="text-red-500 mt-1">
          <FormattedMessage
            id="addShopModal.selectLocation"
            defaultMessage="Select a Location"
          />
        </span>
      )}
    </>
  );
}

function ToggleSwitch({ leftLabel, rightLabel, itemSwitch, setItemSwitch }) {
  const handleToggle = () => {
    setItemSwitch(!itemSwitch);
  };
  const uniqueId = uuidv4();

  return (
    <div className="toggle-switch self-center relative w-3/4 inline-block align-middle select-none text-left">
      <input
        type="checkbox"
        className="toggle-switch-checkbox hidden"
        checked={itemSwitch}
        onChange={handleToggle}
        id={uniqueId}
      />
      <label
        className=" block overflow-hidden border rounded-full"
        htmlFor={uniqueId}
      >
        <span
          className={`block float-left w-1/2 p-2 text-white text-center font-semibold  ${
            itemSwitch ? "bg-sky-500" : "bg-gray-400"
          }`}
        >
          {leftLabel}
        </span>
        <span
          className={`block float-left w-1/2 p-2 text-white text-center font-semibold ${
            itemSwitch ? "bg-gray-400" : "bg-sky-500"
          }`}
        >
          {rightLabel}
        </span>
      </label>
    </div>
  );
}

function CompanyForm(register, errors) {
  const CompanyIntl = useIntl();

  const CompanyNamePlaceholder = CompanyIntl.formatMessage({
    id: "addShopModal.CompanyNamePlaceholder",
    defaultMessage: "Company Name",
  });
  const CompanyNameRequired = CompanyIntl.formatMessage({
    id: "addShopModal.CompanyNameRequired",
    defaultMessage: "Name of the company required",
  });
  const CompanyDescriptionPlaceholder = CompanyIntl.formatMessage({
    id: "addShopModal.CompanyDescriptionPlaceholder",
    defaultMessage: "Company Description (max 100 characters)",
  });
  const CompanyDescriptionRequired = CompanyIntl.formatMessage({
    id: "addShopModal.CompanyDescriptionRequired",
    defaultMessage: "Description of the company required",
  });
  const CompanyDescriptionLength = CompanyIntl.formatMessage({
    id: "addShopModal.CompanyDescriptionLength",
    defaultMessage: "Description must be less than or equal to 100 characters",
  });

  return (
    <>
      <input
        type="text"
        placeholder={CompanyNamePlaceholder}
        {...register("company_name", {
          required: CompanyNameRequired,
        })}
        className="p-2 border border-gray-300 rounded focus:outline-none focus:border-AshinBlue transition"
      />
      {errors.company_name && (
        <p className="text-red-500">{errors.company_name.message}</p>
      )}
      {/* Description */}
      <textarea
        placeholder={CompanyDescriptionPlaceholder}
        {...register("company_description", {
          required: CompanyDescriptionRequired,
          maxLength: {
            value: 100,
            message: CompanyDescriptionLength,
          },
        })}
        maxLength={100}
        className="p-2 border border-gray-300 rounded focus:outline-none focus:border-AshinBlue transition"
      />
      {errors.company_description && (
        <p className="text-red-500">{errors.company_description.message}</p>
      )}
    </>
  );
}

function LocationForm(register, errors) {
  const LocationIntl = useIntl();

  const LocationNamePlaceholder = LocationIntl.formatMessage({
    id: "addShopModal.LocationNamePlaceholder",
    defaultMessage: "Address of the Shop",
  });
  const LocationNameRequired = LocationIntl.formatMessage({
    id: "addShopModal.LocationNameRequired",
    defaultMessage: "Address of the Shop is required",
  });
  const LocationZipPlaceholder = LocationIntl.formatMessage({
    id: "addShopModal.LocationZipPlaceholder",
    defaultMessage: "Zip Code",
  });
  const LocationZipRequired = LocationIntl.formatMessage({
    id: "addShopModal.LocationZipRequired",
    defaultMessage: "zip of the Shop required",
  });
  const LocationCityPlaceholder = LocationIntl.formatMessage({
    id: "addShopModal.LocationCityPlaceholder",
    defaultMessage: "City Name",
  });
  const LocationCityRequired = LocationIntl.formatMessage({
    id: "addShopModal.LocationCityRequired",
    defaultMessage: "City Name required",
  });
  const LocationCountryPlaceholder = LocationIntl.formatMessage({
    id: "addShopModal.LocationCountryPlaceholder",
    defaultMessage: "Country Name",
  });
  const LocationCountryRequired = LocationIntl.formatMessage({
    id: "addShopModal.LocationCountryRequired",
    defaultMessage: "Country Name required",
  });

  return (
    <>
      <div className="flex justify-around">
        <input
          type="text"
          placeholder={LocationNamePlaceholder}
          {...register("location_address", {
            required: LocationNameRequired,
          })}
          className="p-2 mx-1 border w-4/6 border-gray-300 rounded focus:outline-none focus:border-AshinBlue transition"
        />

        <input
          type="text"
          placeholder={LocationZipPlaceholder}
          {...register("location_zip", {
            required: LocationZipRequired,
          })}
          className="p-2 mx-1 border w-2/6 border-gray-300 rounded focus:outline-none focus:border-AshinBlue transition"
        />
      </div>
      {errors.location_address && errors.location_zip && (
        <p className="text-red-500">
          {errors.location_address.message} <br></br>
          {errors.location_zip.message}
        </p>
      )}
      <div className="flex justify-around">
        <input
          type="text"
          placeholder={LocationCityPlaceholder}
          {...register("location_city", {
            required: LocationCityRequired,
          })}
          className="p-2 mx-1 w-3/6 border border-gray-300 rounded focus:outline-none focus:border-AshinBlue transition"
        />

        <input
          type="text"
          placeholder={LocationCountryPlaceholder}
          {...register("location_country", {
            required: LocationCountryRequired,
          })}
          className="p-2 mx-1 w-3/6 border border-gray-300 rounded focus:outline-none focus:border-AshinBlue transition"
        />
      </div>
      {errors.location_country && errors.location_city && (
        <p className="text-red-500">
          {errors.location_country.message} <br></br>{" "}
          {errors.location_city.message}
        </p>
      )}
    </>
  );
}
