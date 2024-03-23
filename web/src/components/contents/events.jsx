import React, { useEffect, useState } from "react";
import { FormattedMessage, useIntl } from "react-intl";
import { format } from "date-fns";
import { Settings, Trash2 } from "lucide-react";
import DeleteModal from "../modals/deleteModal";
import AddEventModal from "../modals/addEventModal";
import UpdateEventModal from "../modals/updateEventModal";
import SlotsEventModal from "../modals/slotsEventModal";

const Events = () => {
  // Display the events and Pagination
  const [events, setEvents] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [maxPages, setMaxPages] = useState(0);
  const pageNumbers = [];
  const pagesToShow = 2;
  const [expanded, setExpanded] = useState(() => window.innerWidth > 980);
  const [searchInput, setSearchInput] = useState("");

  // Handle all the modals
  const [slectedEventIdForDelete, setSelectedEventIdForDelete] = useState(null);
  const [AddModalOpen, AddModalSetOpen] = useState(false);
  const [SelectedEventIdForUpdate, setSelectedEventIdForUpdate] =
    useState(null);
  const [SelectedEventIdForSlots, setSelectedEventIdForSlots] = useState(null);
  const intl = useIntl();

  const searchPlaceholder = intl.formatMessage({
    id: "events.searchPlaceholder",
    defaultMessage: "Search by name ...",
  });

  // Fetch the users from the API
  const fetchEvents = () => {
    // let url =
    //   searchInput != ""
    //     ? `http://127.0.0.1:5000/user/page/${currentPage}/search/${searchInput}`
    //     : `http://127.0.0.1:5000/user/page/${currentPage}`;
    // fetch(url)
    //   .then((response) => response.json())
    //   .then((data) => {
    //     setUsers(data.users);
    //     const usersLength = data.users.length;
    //     for (let i = 0; i < 10 - usersLength; i++) {
    //       data.users.push({
    //         id: `placeholder-${i}`,
    //         first_name: "",
    //         last_name: "",
    //         email: "",
    //         status: null,
    //         role: [],
    //       });
    //     }
    //     setMaxPages(data.max_pages);
    //   })
    //   .catch((error) => {
    //     console.error("Error fetching users:", error);
    //   });

    let events_json = [
      {
        id: 1,
        title: "Introduction to Programming",
        description:
          "Learn the basics of programming with Python, covering variables, loops, and functions.",
        dateTime: "2024-03-20T10:00:00",
        maxSlot: 30,
        group: 0,
        type: {
          id: 2,
          name: "Dog Development",
        },
        location: "Room 101, Tech Building",
        users: [
          {
            email: "alice@example.com",
            id: 1,
          },
          {
            email: "bob@example.com",
            id: 2,
          },
          {
            email: "alice@example.com",
            id: 1,
          },
          {
            email: "bob@example.com",
            id: 2,
          },
          {
            email: "alice@example.com",
            id: 1,
          },
          {
            email: "bob@example.com",
            id: 2,
          },
          {
            email: "alice@example.com",
            id: 1,
          },
          {
            email: "bob@example.com",
            id: 2,
          },
          {
            email: "alice@example.com",
            id: 1,
          },
          {
            email: "bob@example.com",
            id: 2,
          },
          {
            email: "alice@example.com",
            id: 1,
          },
          {
            email: "bob@example.com",
            id: 2,
          },
          {
            email: "alice@example.com",
            id: 1,
          },
          {
            email: "bob@example.com",
            id: 2,
          },
        ],
      },
      {
        id: 2,
        title: "Advanced Web Development",
        description:
          "Dive deep into web technologies with this course on React, Node.js, and MongoDB.",
        dateTime: "2024-03-22T14:00:00",
        group: 1,
        type: {
          id: 1,
          name: "Web Development",
        },
        maxSlot: 25,
        location: "Room 202, Tech Building",
        users: [
          {
            email: "alice@example.com",
            id: 3,
          },
          {
            email: "bob@example.com",
            id: 4,
          },
        ],
      },
      {
        id: 3,
        title: "Game Development",
        description:
          "Create your own games with Unity, covering 2D and 3D game development.",
        dateTime: "2024-01-25T17:20:00",
        maxSlot: 3,
        group: 2,
        type: {
          id: 3,
          name: "Cloud Development",
        },
        location: "Room 201, ARK Building",
        users: [
          {
            email: "freddy@example.com",
            id: 5,
          },
          {
            email: "Cait@example.com",
            id: 6,
          },
          {
            email: "Vi@example.com",
            id: 7,
          },
        ],
      },
    ];

    setEvents(events_json);
    const eventsLength = events.length;
    for (let i = 0; i < 10 - eventsLength; i++) {
      events.push({
        id: eventsLength + i, // Assuming numerical IDs for simplicity
        title: `Placeholder Course ${i}`,
        description: "",
        dateTime: "",
        group: 0,
        type: {
          id: 2,
          name: "Dog Development",
        },
        maxSlot: 0,
        location: "",
        users: [], // Keeping users array to match structure
      });
    }
    setMaxPages(1);

    console.log(events);
  };

  // Remove a user from the API
  const deleteEvent = (EventId) => {
    // fetch(`http://127.0.0.1:5000/user/${EventId}`, {
    //   method: "DELETE",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    // }).then((response) => {
    //   if (!response.ok) {
    //     throw new Error("Network response was not ok");
    //   }
    // Refresh the users list and quit the modal
    fetchEvents();
    setSelectedEventIdForDelete(null);
    // });
  };

  // Set the user id to delete
  const handleDeleteClick = (EventId) => {
    setSelectedEventIdForDelete(EventId);
  };

  // Set the user id to update
  const handleUpdateClick = (EventId) => {
    setSelectedEventIdForUpdate(EventId);
  };

  // Set the user id to update
  const handleSlotsClick = (EventId) => {
    setSelectedEventIdForSlots(EventId);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setSearchInput(e.target.value);
    if (e.keyCode == 13) {
      fetchEvents();
    }
  };

  const handleClickSearch = (e) => {
    if (e.type == "click" || e.keyCode == 13) fetchEvents();
  };

  // Fetch the users when we change Page
  useEffect(() => {
    fetchEvents();
  }, [currentPage]);

  // Function to handle window resize
  useEffect(() => {
    const handleResize = () => {
      setExpanded(window.innerWidth > 980);
    };
    handleResize();
    window.addEventListener("resize", handleResize);
  });

  // Array of pagination [1,2,3,...,maxPages]
  let startPage = Math.max(currentPage - pagesToShow, 1);
  let endPage = Math.min(currentPage + pagesToShow, maxPages);
  if (startPage !== 1) {
    pageNumbers.push(1);
    if (startPage > 2) pageNumbers.push("...");
  }
  for (let i = startPage; i <= endPage; i++) {
    pageNumbers.push(i);
  }
  if (endPage < maxPages) {
    if (endPage < maxPages - 1) pageNumbers.push("...");
    pageNumbers.push(maxPages);
  }

  return (
    <div className={`h-screen p-8 pt-8 ${expanded ? "mx-6" : "mx-1"}`}>
      <div className="flex mb-6 items-center">
        <h1
          className={`${
            expanded ? "text-3xl" : "text-2xl"
          } font-bold flex-grow`}
        >
          <FormattedMessage
            id="event.eventsManagement"
            defaultMessage="events Management"
          />
        </h1>
        <button
          className={`text-base bg-gradient-to-tr from-AshinBlue-light to-AshinBlue-dark text-white px-4 ${
            expanded ? "py-3" : "py-2"
          } rounded transition hover:opacity-90 text-sm`}
          onClick={() => {
            AddModalSetOpen(true);
          }}
        >
          <FormattedMessage
            id="event.addANewEvent"
            defaultMessage="+ Add a new event"
          />
        </button>
        <AddEventModal
          AddModalOpen={AddModalOpen}
          AddModalSetOpen={() => AddModalSetOpen(false)}
          fetchUsers={fetchEvents}
        />
      </div>
      {/* Searchbar */}
      <div className="flex gap-4 mb-6 items-stretch">
        <input
          type="text"
          placeholder={searchPlaceholder}
          className="p-2 border border-gray-300 rounded flex-grow focus:outline-none focus:border-AshinBlue transition"
          onChange={handleSearch}
          onKeyDown={handleClickSearch}
          value={searchInput}
        />
        <button
          className="bg-gradient-to-tr from-AshinBlue-light to-AshinBlue-dark text-white px-4 py-2 rounded hover:opacity-90 transition self-end"
          onClick={handleClickSearch}
        >
          <FormattedMessage id="users.search" defaultMessage="Search" />
        </button>
      </div>
      {/* List of Users */}
      <div className="overflow-x-auto">
        {/* Table of Users */}
        <table className="w-full text-left">
          <thead className="bg-gray-100">
            <tr>
              <th className={` p-4 w-1/4  max-w-xs`}>
                {" "}
                <FormattedMessage id="event.title" defaultMessage="Title" />
              </th>
              <th className={` p-4 w-1/12 text-center max-w-xs`}>
                {" "}
                <FormattedMessage id="event.group" defaultMessage="Group" />
              </th>
              {expanded && (
                <th className="p-4 w-1/6 max-w-xs text-center">
                  {" "}
                  <FormattedMessage id="event.type" defaultMessage="Type" />
                </th>
              )}{" "}
              {expanded && (
                <th className="p-4 w-1/6 max-w-xs text-center">
                  {" "}
                  <FormattedMessage
                    id="event.dateTime"
                    defaultMessage="Date & Time"
                  />
                </th>
              )}{" "}
              <th className="p-4 w-1/12 max-w-xs text-center">
                {" "}
                <FormattedMessage id="event.maxSlots" defaultMessage="Slots" />
              </th>
              <th className="p-4 w-1/4 max-w-xs text-center">
                {" "}
                <FormattedMessage
                  id="event.location"
                  defaultMessage="Location"
                />
              </th>
              <th className="w-1/12">
                {" "}
                <FormattedMessage id="users.actions" defaultMessage="Actions" />
              </th>
            </tr>
          </thead>
          <tbody>
            {/* For each user ... */}
            {events.map((event) => (
              <tr key={event.id} className="border-b">
                {/* title & dataTime */}
                {!expanded && (
                  <td className="text-sm">
                    {event.title}
                    <br></br>
                    <span className="text-slate-500">
                      {" "}
                      {format(new Date(event.dateTime), "yy/MM/dd HH'H'mm ")}
                    </span>
                  </td>
                )}{" "}
                {expanded && (
                  <td className="p-4 w-1/6 max-w-xs whitespace-nowrap overflow-hidden text-ellipsis">
                    {event.title}
                  </td>
                )}{" "}
                {/* Group */}
                <td
                  className={`py-4 text-center ${!expanded ? "text-sm" : ""}`}
                >
                  <span
                    className={`bg-gradient-to-tr px-3 py-1 rounded-full text-white ${
                      event.group === 1
                        ? "from-blue-300 to-blue-600"
                        : event.group === 2
                        ? "from-yellow-300 to-yellow-600"
                        : "from-orange-300 to-orange-600"
                    }`}
                  >
                    {event.group === 1
                      ? "Activity"
                      : event.group === 2
                      ? "event"
                      : "Service"}
                  </span>
                </td>
                {/* Type */}
                {expanded && (
                  <td
                    className={`py-4 text-center ${!expanded ? "text-sm" : ""}`}
                  >
                    {event.type.name}
                  </td>
                )}{" "}
                {expanded && (
                  <td className={`text-center`}>
                    {" "}
                    {format(new Date(event.dateTime), "yy/MM/dd HH'H'mm ")}
                  </td>
                )}{" "}
                {/* max_slot */}
                <td
                  className={` py-4 text-center ${!expanded ? "text-sm" : ""}`}
                >
                  <button
                    className={`bg-gradient-to-tr text-white px-2 py-1 rounded hover:opacity-90 transition self-end  ${
                      event.users.length != event.maxSlot
                        ? "from-green-300 to-green-600"
                        : "from-red-300 to-red-600"
                    } `}
                    onClick={() => handleSlotsClick(event.id)}
                  >
                    {event.users.length}/{event.maxSlot}
                  </button>
                  {SelectedEventIdForSlots === event.id && (
                    <SlotsEventModal
                      SlotsModalOpen={SelectedEventIdForSlots === event.id}
                      SlotsModalSetOpen={() => setSelectedEventIdForSlots(null)}
                      event={event}
                      fetchUsers={fetchEvents}
                    />
                  )}
                </td>
                {/* location */}
                <td
                  className={`py-4 text-center ${!expanded ? "text-sm" : ""}`}
                >
                  {event.location}
                </td>
                {/* actions */}
                <td>
                  {event.title != null && (
                    <>
                      <button
                        className="text-blue-600 hover:text-blue-800 mr-2"
                        onClick={() => handleUpdateClick(event.id)}
                      >
                        {<Settings size={20} />}
                      </button>
                      {SelectedEventIdForUpdate === event.id && (
                        <UpdateEventModal
                          UpdateModalOpen={
                            SelectedEventIdForUpdate === event.id
                          }
                          UpdateModalSetOpen={() =>
                            setSelectedEventIdForUpdate(null)
                          }
                          event={event}
                          fetchUsers={fetchEvents}
                        />
                      )}
                      <button
                        className="text-red-600 hover:text-red-800 mr-2"
                        onClick={() => handleDeleteClick(event.id)}
                      >
                        {<Trash2 size={20} />}
                      </button>
                      <DeleteModal
                        open={slectedEventIdForDelete === event.id}
                        onClose={() => setSelectedEventIdForDelete(null)}
                        fetchUsers={() => deleteEvent(event.id)}
                      />{" "}
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Pagination */}
      <div className="flex justify-center mt-4">
        {pageNumbers.map((pageNum, index) =>
          pageNum === "..." ? (
            <span key={index} className="mx-1 px-4 py-2">
              ...
            </span>
          ) : (
            <button
              key={pageNum}
              className={`mx-1 px-4 py-2  bg-gray-200 rounded bg-gradient-to-tr hover:from-AshinBlue-light hover:to-AshinBlue-dark hover:text-white ${
                currentPage === pageNum
                  ? "from-AshinBlue-light to-AshinBlue-dark text-white"
                  : ""
              }`}
              onClick={() => setCurrentPage(pageNum)}
            >
              {pageNum}
            </button>
          )
        )}
      </div>
    </div>
  );
};

export default Events;