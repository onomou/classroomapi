class ClassroomObject:
    def __init__(self, attributes):
        for attribute, value in attributes.items():
            self.__setattr__(attribute, value)
    
    def __repr__(self):  # pragma: no cover
        classname = self.__class__.__name__
        attrs = ", ".join(
            [
                "{}={}".format(attr, val)
                for attr, val in self.__dict__.items()
                if attr != "attributes"
            ]
        )  # noqa
        return "{}({})".format(classname, attrs)

    def __iter__(self):
        """
        Enables iteration over object attributes.

        Yields:
            str: Attribute name.
        """
        for key in self.__dict__:
            yield key

    def __len__(self):
        """
        Returns the number of attributes on the object.

        Returns:
            int: Number of attributes.
        """
        return len(self.__dict__)
    
    